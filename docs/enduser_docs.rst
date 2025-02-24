Creating ojr endpoint
---------------------

ojr specific 
#. ui_app_trmap: is a list of triplets that define mapping from uistate to appstate 
   - each triple consists of 
     - uipath
     - appstate path
     - modifier
       

#. action_module a module with functions
   - each function is associated with bunch of appstate path
   - function is executed if there is a change in the value of the appstate path
   - arguments of the function


general webpage argument

#. rendering_type
   - keep the default CSR
     - which is client side rendering

#. post_init
     - function invoked after the webpage class is initialized

#. path_guards
   - don't worry for now
     
     


   
   .. code-block::
   
      ui_app_trmap = [('/color_choice', '/update_sty_hcobj/selected_color', None),
      endpoint = ojr.create_endpoint(f"wp_csv_schema_metadata_{label}",
                                   [form_box

                                       ],
                                   ui_app_trmap_iter = ui_app_kmap,
                                   action_module = actions,
                                   rendering_type="CSR",
                                   csr_bundle_dir="hyperui",
                                   path_guards = path_guards,
                                   post_init = post_init,
                                   head_html =  """<script src="https://cdn.tailwindcss.com"></script> """,
                                   reactctx = [ojr.Ctx("/wp_redirect", ojr.isstr, ojr.UIOps.REDIRECT)]
                                   )
