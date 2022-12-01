The vocabulary
+++++++++++++++
- appctx
  a misnomer. Should be appChangeCtx. Refers to path in appstate that have new/changed value
  

The react webpage data-structures 
++++++++++++++++++++++++++++++++++
- appstate
  
- uistate
  
- ui_app_trmap
  
- appctx_uiupdate_map
  tells which ui elements should be updated based on appctx
  
- app_actions_trmap
  which actions are associated with appstate change context
  
- action  


Initializations
++++++++++++++++
- appctx_uiupdate_map
  look for kwargs reactctx in the constructor of the ui components.
  
  


- app_actions_trmap
  from docstring of functions in action module
  

The execution flow
+++++++++++++++++++
- Decorator ReactDomino calls
  - wp.update_uistate(sspath, svalue)
  - up.update_loop

- wp.update_uistate(spath, svalue)
  
