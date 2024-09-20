from ofjustpy import app_code_introspect as aci

from .react import ReactTag_AppstateUpdate, ReactTag_BackendAction, ReactTag_UI, make_react, TaskStack, LoopRunner, UpdateAppStateAndUI, OpStatus, CfgLoopRunner

ReactDomino = CfgLoopRunner

from .webpage import make_opaque_dict,  AttrMeta, eq_op, isstr, Ctx, UIOps,  ResponsiveStatic_CSR_WebPage, ResponsiveStatic_SSR_WebPage

from ofjustpy import create_endpoint_impl
def default_page_builder(key=None, childs=[], rendering_type="CSR", **kwargs):
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

    
def get_page_builder():
    if aci.page_builder is not None:
        return aci.page_builder
    
    return default_page_builder


def create_endpoint(key, childs, **kwargs):
    
        
    page_builder = get_page_builder()
    wp_template = page_builder(key, childs, **kwargs)
    wp_endpoint = create_endpoint_impl(wp_template)
    return wp_endpoint



__version__ = "0.1.0"
