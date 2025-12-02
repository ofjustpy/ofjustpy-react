"""
attrmeta is a graball module for all metadata about chartjs attributes
"""
import logging
from typing import Any, NamedTuple
import os
import sys
from aenum import Enum, auto

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

import inspect

from addict_tracking_changes import Dict
#import kavya as kv

from collections import namedtuple
from py_tailwind_utils import (dget,
                               dnew,
                               dsearch,
                               dpop,
                               dictWalker,
                               )
from dpath import PathNotFound
from ofjustpy.htmlcomponents_impl import id_assigner
from ofjustpy.WebPage_TF import gen_WebPage_type
from ofjustpy.generate_WebPage_response_mixin import (ResponsiveStatic_SSR_ResponseMixin,
                                                   ResponsiveStatic_CSR_ResponseMixin
                                                   )
def is_mod_function(mod, func):
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def list_functions(mod):
    return filter(lambda func, mod=mod: is_mod_function(mod, func),
                  mod.__dict__.values()
                  )



def make_opaque_dict(adict: dict, name="anon"):
    fields = adict.keys()
    tpl_cls = namedtuple(name, fields)
    return  tpl_cls(*adict.values())


class UIAppCtx(NamedTuple):
    uipath: Any
    apppath: Any
    valueop: Any
    
class AttrMeta(NamedTuple):
    """
    metadata about ui component
    """
    default: Any
    appstate_context: Any

# class AttrMetaUIAppstate(NamedTuple):
#     ui_context:Any
# _cfg = cfg_UI_appstate_transition_matrix = Dict(track_changes=True)
# _cfg.dbsession.id  = AttrMetaUIAppstate("/dbsess

def eq_op(val):
    return lambda x, val=val: x == val


def isstr(val):
    return isinstance(val, str)



class Ctx(NamedTuple):
    apppath: Any
    condition: Any
    uiop: Any
    
class UIOps(Enum):
    DISABLE = auto()
    ENABLE = auto()
    UPDATE_NOTICEBOARD = auto()
    APPEND_CLASSES = auto()
    #update text attribute of a class
    UPDATE_TEXT = auto()

    #redirect to new page
    REDIRECT = auto()

    # call deck.bring_to_front
    DECK_SHUFFLE = auto()

    DEBUG = auto()
    
    UPDATE_CHART = auto()
    
def components_in_appstate_changectx(apppath, val,  appctx_uiupdate_map):
    """
    which components have registered for the change.
    returns components path in cfgCM
    """
    
    try:
        spath, appchangectx = dget(appctx_uiupdate_map,  apppath)
        if appchangectx.condition(val):
            yield spath, appchangectx
    except Exception as e:
        logger.debug(f"{apppath} not in appctx_uiupdate_map: skipping update of the ui")
        #raise e
                    
def uiops_for_appstate_change_ctx_kpath(kpath, val, appctx_uiupdate_map):
    """
    update cfgCM in response to  changes in appstate at kpath
    """

    #logger.debug(f"evaluation ctx: apppath:{kpath} val={val}")
    affected_uis = [
        _ for _ in components_in_appstate_changectx(kpath, val,  appctx_uiupdate_map)]
    for spath, appchangectx in affected_uis:
        # TODO: we should change something for sure.
        # the bojective is to update the ui with newly added data model
        # dget(stubStore, path).target.update(val)
        # print(f"Que {path} {kpath} {val} {cm}")
        # match ctx.uiop:
        #     case UIOps.ENABLE:
        #         #dset(cfg_CM, path, "enabled")
        #         #am.is_enabled = True
        #     case UIOps.DISABLE:
        #         #dset(cfg_ui, path, "disabled")
        # logger.info(
        #     f"changing ui for {spath} with uiop {appchangectx.uiop}")

        yield spath, val, appchangectx.uiop




#def uiops_for_appstate_change_ctx(appstate, appctx_uiupdate_map, new_inactive_kpaths=[], path_guards = None):
def uiops_for_appstate_change_ctx(appstate_all_changed_paths,
                                  appctx_uiupdate_map,
                                  appstate,
                                  new_inactive_kpaths=[],
                                  path_guards = None):
    
    """
    a change on frontend/browser is recorded in cfg_ui and in appstate.
    update cfg_CM based on dependency
    """
    #all_changed_paths = [_ for _ in appstate.get_changed_history(path_guards = path_guards)]
    #logger.debug (f"appstate:all_changed_paths {all_changed_paths}")
    for kpath in appstate_all_changed_paths:
        new_val = dget(appstate, kpath)
        # logger.debug(
        #     f"{kpath} has changed in appstate to  new_value={new_val}")
        yield from uiops_for_appstate_change_ctx_kpath(
            kpath, new_val, appctx_uiupdate_map)

    for kpath in new_inactive_kpaths:
        logger.debug("inactive paths are not implemented yet")
        pass

    #logger.debug("done update ui for appstate cha...")


#initialize ui_app_trmap from app_ui_trmap    
def refresh_uistate(app_ui_trmap, uistate, stubStore):
    """
    this can be made generic for sure. 
    path_filter: condition to avoid changed path

    """
    logger.debug("=========== start update_cfg_ui  ===============")
    # remove everything thats changed and put it
    # back in only the active ones: this enables deletion
    inactive_kpaths = set()
    for kpath in app_ui_trmap.get_changed_history():
        logger.debug(f"path {kpath} changed in cfgattrmeta")
        try:
            # logger.debug("what bakwas")
            # opts = jsbeautifier.default_options()
            # logger.debug(jsbeautifier.beautify(json.dumps(cjscfg), opts))
            dpop(uistate, kpath)
            inactive_kpaths.add(kpath)
        except PathNotFound as e:
            logger.info(f"skipping: {kpath} not found in uistate {e}")
            pass  # skip if path is not in chartcfg
        pass
    for kpath in app_ui_trmap.get_changed_history():

        #evalue = get_defaultVal(dget(cfg_CM, kpath))
        evalue = dget(app_ui_trmap, kpath).default
        dnew(uistate, kpath, evalue)
        if kpath in inactive_kpaths:
            inactive_kpaths.remove(kpath)
        logger.debug(f"path {kpath} updated with {evalue} in uistate")

    # cfgattrmeta.clear_changed_history()
    if inactive_kpaths:
        logger.debug(f"paths that became inactive: {inactive_kpaths}")
    logger.debug("=========== done refresh_uistate  ===============")
    return inactive_kpaths



class WebPage_React_Mixin:
    def __init__(self, *args, **kwargs
                 # session_manager=None,
                 # path_guards = None,
                 # #enable_quasar=False,
                 # action_module=None,
                 ):
        """
        cfg_CM: config component meta
        action_module: module with all the actions/functions that defines reaction. 
        """
        global logger
        self.session_manager = kwargs.get('session_manager')
        
        #super().__init__(session_manager=session_manager, **kwargs)

        self.appstate = self.session_manager.appstate
        self.stubStore = self.session_manager.stubStore
        self.path_guards = kwargs.get('path_guards', None)
        self.action_module = kwargs.get('action_module', None)
        ui_app_trmap_iter = kwargs.get('ui_app_trmap_iter', [])
        
        
        # ============ build appctx to action trigger map ============
        
        self.app_actions_trmap = Dict(track_changes=True)
        if self.action_module:
            for afunc in list_functions(self.action_module):
                if inspect.getdoc(afunc) is None:
                    continue
                doctoks = inspect.getdoc(afunc).split()

                if doctoks:
                    if 'appctx' in doctoks[0]:
                        spaths = doctoks[0].split("=")[1]
                        for spath in spaths.split(":"):
                            dnew(self.app_actions_trmap, spath, [afunc])

        # build appctx to ui update map
        # Get back to this soon
        self.appctx_uiupdate_map = Dict(track_changes=True)
        for spath, stub in dictWalker(self.stubStore):

            if getattr(stub, 'kwargs', None):
                if 'reactctx' in stub.kwargs:
                    for appchangectx in stub.kwargs.get('reactctx'):#TODO: what if apppath already exists
                        dnew(self.appctx_uiupdate_map, appchangectx.apppath, (spath, appchangectx))
            else:
                
                pass
                
                        

        logger.debug("reactctx collected ")
        logger.debug(self.appctx_uiupdate_map)
        
        #stores the value/state of active/input ui components
        self.uistate = Dict(track_changes=True)

        #mapping from uistate changes to appstate 
        self.ui_app_trmap = Dict(track_changes=True)
        for uipath, apppath, valop  in ui_app_trmap_iter:
            dnew(self.ui_app_trmap, uipath, (apppath, valop))

        #refresh_uistate(self.appctx_uiupdate_map, self.uistate, self.stubStore)
        self.ui_app_trmap.clear_changed_history()
        self.uistate.clear_changed_history()
        self.appctx_uiupdate_map.clear_changed_history()
        logger.debug("----appctx_uiupdate_map----")
        logger.debug(self.appctx_uiupdate_map)
        logger.debug("----ui_app_trmap----")
        logger.debug(self.ui_app_trmap)
        logger.debug("----app_actions_trmap----")
        logger.debug(self.app_actions_trmap)

        logger.debug("----appstate----")
        logger.debug(self.appstate)
        logger.debug("----uistate----")
        logger.debug(self.uistate)

    def update_uistate(self, spath, value):
        """
        set value of cfg_ui at spath value
        """
        try:
            old_val = dget(self.uistate, spath)
            logger.debug(
                f"Phase 1: update-uistate:   update ui: key/path={spath};  old_val = {old_val};  new_value= {value}")
            # dupdate has issues; dnew works just as well; 
            # dupdate(self.uistate, spath, value)
            # debug it 
            dnew(self.uistate, spath, value)
            
        except KeyError as e:
            dnew(self.uistate, spath, value)
            logger.debug(
                f"Phase 1:update_uistate:add-new-path-and-value: update key={spath}, value={value}")
        


    def build_list(self):
        return super().build_list()
    
    async def update_loop(self):
        """
        user has changed the state of ui input component.
        this has led to change in values in  uistate.

        in this function we loop:
        1. update appstate for uistate changes via ui_app_trmap
        2. perform actions
        3. update ui

        """

        logger.debug("*********** Begin Phase 2: update appstate (from ui)")
        
        for _ in self.uistate.get_changed_history():
            uival = dget(self.uistate, _)
            logger.debug(f"             changed ui path: {_}")
            app_path = None
            appval = None
            # dsearch returns an iterator
            if list(dsearch(self.ui_app_trmap, _)):
                app_path, value_tranformer = dget(self.ui_app_trmap, _)
                appval = uival
                if value_tranformer:
                    appval = value_tranformer(uival)
            elif list(dsearch(self.appstate, _)):
                app_path = _
                appval = uival


            if app_path:
                if list(dsearch(self.appstate, _)):
                    logger.debug(f"            matching app path:update: {app_path} with appval={appval}")
                    # dupdate has issues with clear; dnew works fine
                    #dupdate(self.appstate, app_path,  appval)
                    dnew(self.appstate, app_path,  appval)
                    logger.debug(f"            post-update-val {app_path} with appval={appval} : {dget(self.appstate, app_path)}", )
                    
                                 
                else:
                    logger.debug(f"            matching app path:new: {app_path} with appval={appval}")
                    dnew(self.appstate, app_path,  appval)
                    logger.debug(f"            post-new-val {app_path} with appval={appval} {dget(self.appstate, app_path)}")
                
            else:
                logger.debug(f"path {_} does not exists in appstate or in ui_app_trmap: skipping")
                
 
        # perform actions for updated appstate
        self.uistate.clear_changed_history()
        logger.debug("*********** End Phase 2: update appstate")

        for bigloop in range(3):
            logger.debug(f"*********** Begin Phase 3: trigger actions; bigloop:{bigloop}")
            logger.debug(f"            collect all appstate changes")

            appstate_all_changed_paths = [_ for _ in self.appstate.get_changed_history(path_guards = self.path_guards)]
            self.appstate.clear_changed_history()
                                                             
            logger.debug(f"all appstate changes {appstate_all_changed_paths}")
            logger.debug (f"            trigger actions for appstate changes : ")
            for kpath in appstate_all_changed_paths :
                logger.debug (f"            visiting appstate path : {kpath}")
                kval = dget(self.appstate, kpath)
                if list(dsearch(self.app_actions_trmap, kpath)):

                    #TODO: handle series of actions
                    action_fns = dget(self.app_actions_trmap, kpath)
                    logger.debug(f"       actions invoked: {action_fns}" )
                    for action_fn in action_fns:
                        action_fn(self.appstate, kval, self)

                pass

            # actions and cfg_ui have updated appstate  ==> try to update cfg_CM and the ui
            logger.debug("*********** End Phase 3: trigger actions")

            logger.debug("*********** Begin Phase 4: Update UI")
            for spath,  kval, uiop in uiops_for_appstate_change_ctx(appstate_all_changed_paths, self.appctx_uiupdate_map, self.appstate):
                logger.debug(f" visiting app path: {spath} uiop:{uiop} val:{kval}")
                target_dbref = dget(self.stubStore, spath).target
                match uiop:
                    case UIOps.ENABLE:
                        target_dbref.remove_class("disabled")
                        pass
                    case UIOps.DISABLE:
                        pass
                    case UIOps.UPDATE_NOTICEBOARD:
                        pass
                    case UIOps.DECK_SHUFFLE:
                        target_dbref.bring_to_front(kval)
                    case UIOps.UPDATE_CHART:
                        logger.debug(f"Update chart called with stub path/key: {spath} {kval}")
                        target_dbref.update_chart(kval[0], kval[1])

                        #target_dbref.update_chart(kval)                     
                    case UIOps.UPDATE_TEXT:
                        logger.debug("in uiops.update_text: ")
                        #TODO: when it is text vs. placeholder
                        match target_dbref.html_tag:
                            case 'input':
                                 target_dbref.placeholder = kval
                            case 'span':
                                 target_dbref.text = kval
                            case _:
                                 print("unkown how to update text for : ", target_dbref.html_tag)
                    case UIOps.REDIRECT:
                        logger.debug(f"in uiops.redirect for : target_dbref, " ", {target_dbref.id}, " ",  {kval}" )
                        await target_dbref.redirect_to_url(kval)
                        
                        #target_dbref.redirect = kval
                        #TODO: when it is text vs. placeholder
                        #target_dbref.placeholder = kval
                    case UIOps.DEBUG:
                        logger.debug(f"I am at debug with kval  = {kval}")
            logger.debug("*********** End Phase 4: Update UI")

        self.appstate.clear_changed_history()
        self.uistate.clear_changed_history()
        
        pass

    
ResponsiveStatic_CSR_WebPage = id_assigner(gen_WebPage_type(mutableShellMixins = [WebPage_React_Mixin]))

ResponsiveStatic_SSR_WebPage = id_assigner(gen_WebPage_type(generate_WebPage_response_mixin = ResponsiveStatic_SSR_ResponseMixin,
                                                mutableShellMixins = [WebPage_React_Mixin]))
