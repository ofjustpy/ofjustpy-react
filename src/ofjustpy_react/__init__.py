from ofjustpy import (app_code_introspect as aci,
                    create_endpoint_impl
                   )

from .react import ReactTag_AppstateUpdate, ReactTag_BackendAction, ReactTag_UI, make_react, TaskStack, LoopRunner, UpdateAppStateAndUI, OpStatus, CfgLoopRunner

ReactDomino = CfgLoopRunner

from .webpage import make_opaque_dict,  AttrMeta, eq_op, isstr, Ctx, UIOps,  ResponsiveStatic_CSR_WebPage, ResponsiveStatic_SSR_WebPage


def default_pagecontent_builder(key=None, childs=[], rendering_type="CSR", **kwargs):
    # by default we perform client side rendering
    # its more powerful -- incorporates svelte components

    if rendering_type == "CSR":
        return ResponsiveStatic_CSR_WebPage(
            key=key,
            childs=childs,
            cookie_state_attr_names=aci.the_starlette_app.cookie_state_attr_names,
            **kwargs,
        )
    if rendering_type == "SSR":
        return ResponsiveStatic_SSR_WebPage(key=key,
                                                    childs =childs,
                                                    cookie_state_attr_names=aci.the_starlette_app.cookie_state_attr_names,
                                                    
                                                    **kwargs
                                                   )

    assert False

    
def get_pagecontent_builder():
    if aci.pagecontent_builder is not None:
        return aci.pagecontent_builder
    
    return default_pagecontent_builder


def create_endpoint(key, childs, **kwargs):
    pagecontent_builder = get_pagecontent_builder()
    wp_template = pagecontent_builder(key, childs, **kwargs)
    wp_endpoint = create_endpoint_impl(wp_template)
    return wp_endpoint



__version__ = "0.1.0"
