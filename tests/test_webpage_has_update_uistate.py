import ofjustpy as oj
import ofjustpy_react as ojr
from py_tailwind_utils import *

ui_app_trmap = []

btn = oj.Mutable.Button(key="abtn", text="Click me", twsty_tags=[bg/green/100])

tlc = oj.Mutable.Container(key="tlc", childs = [btn])

wp_template = ojr.WebPage(key="ojr_Webpage",
                          childs=[tlc],
                          ui_app_trmap_iter = ui_app_trmap
                          )
# wp_template = oj.Mutable.WebPage(key="ojr_Webpage",
#                           childs=[btn],
#                           )
wp_endpoint = oj.create_endpoint_impl(wp_template,

                                      )
app = oj.load_app()
request = Dict()
request.session_id = "abc"
wp = wp_endpoint(request)

#oj.add_jproute("/index", wp_endpoint)



