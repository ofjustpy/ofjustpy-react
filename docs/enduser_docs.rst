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


#. On making the ui event handler reactive
   - decorate the function
     .. code-block
	@ojr.ReactDomino
	async def on_utility_class_input(dbref, msg, to_ms):

   - return a list of tuples
     - each tuple has
       - uistate path as key
       - and a value
	 
     .. code-block::

	return [("/callback_mouseenter_hcobj", selected_hcobj),
                ("/update_target_wp", None)
                ]


#. trigger ui event-handler and react dominio

   
   .. code-block::
      from starlette.testclient import TestClient

      async def  main():
	  with TestClient(app) as client:
	      response = client.get("/x")
	      response = client.get(f'/styedit')
	      # get hold of session_manager

	      sm =  list(oj.tracker.session_manager_store.values())[0]
	      ss = sm.stubStore
	      appstate = sm.appstate

	      page_id="cluster_dashboard"
              styeditor_wp = ss[page_id].target
      msg = Dict()
      msg.page = styeditor_wp
      def to_stubStore(x, stubStore=ss):
      return dget(stubStore, x.id).target

      # 1st click: Test Page
      await click_eh(lbtn0, msg, to_stubStore)           # Run the main function




      from anyio import run

      # Run the async functions
      if __name__ == "__main__":
      with TestClient(app) as client:
      run(main)


#. set function change-triggers
   - i.e. functions that get executed when
     - there is change in appstate value

   - define the function in action_module
   - provide docstring 
   .. code-block::

      def on_mouseclick_hcobj(appstate, arg, wp):
           """
	   appctx=/update_sty_hcobj/clicked_hcobj
	   """
	   
