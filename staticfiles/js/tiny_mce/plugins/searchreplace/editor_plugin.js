(function(){tinymce.create("tinymce.plugins.SearchReplacePlugin",{init:function(a,c){function b(d){a.windowManager.open({file:c+"/searchreplace.htm",width:420+parseInt(a.getLang("searchreplace.delta_width",0)),height:170+parseInt(a.getLang("searchreplace.delta_height",0)),inline:1,auto_focus:0},{mode:d,search_string:a.selection.getContent({format:"text"}),plugin_url:c})}a.changeCommand("mceSearch",function(){b("search")});a.addCommand("mceReplace",function(){b("replace")});a.addButton("search",{title:"searchreplace.search_desc",cmd:"mceSearch"});a.addButton("replace",{title:"searchreplace.replace_desc",cmd:"mceReplace"});a.addShortcut("ctrl+f","searchreplace.search_desc","mceSearch")},getInfo:function(){return{longname:"Search/Replace",author:"Moxiecode Systems AB",authorurl:"http://tinymce.moxiecode.com",infourl:"http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/searchreplace",version:tinymce.majorVersion+"."+tinymce.minorVersion}}});tinymce.PluginManager.add("searchreplace",tinymce.plugins.SearchReplacePlugin)})();
