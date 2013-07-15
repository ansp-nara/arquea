/**
 * editor_plugin_src.js
 *
 * Copyright 2009, Moxiecode Systems AB
 * Released under LGPL License.
 *
 * License: http://tinymce.moxiecode.com/license
 * Contributing: http://tinymce.moxiecode.com/contributing
 */

(function() {
	tinymce.create('tinymce.plugins.XHTMLXtrasPlugin', {
		init : function(ed, url) {
			// Register commands
			ed.changeCommand('mceCite', function() {
				ed.windowManager.open({
					file : url + '/cite.htm',
					width : 350 + parseInt(ed.getLang('xhtmlxtras.cite_delta_width', 0)),
					height : 250 + parseInt(ed.getLang('xhtmlxtras.cite_delta_height', 0)),
					inline : 1
				}, {
					plugin_url : url
				});
			});

			ed.changeCommand('mceAcronym', function() {
				ed.windowManager.open({
					file : url + '/acronym.htm',
					width : 350 + parseInt(ed.getLang('xhtmlxtras.acronym_delta_width', 0)),
					height : 250 + parseInt(ed.getLang('xhtmlxtras.acronym_delta_width', 0)),
					inline : 1
				}, {
					plugin_url : url
				});
			});

			ed.changeCommand('mceAbbr', function() {
				ed.windowManager.open({
					file : url + '/abbr.htm',
					width : 350 + parseInt(ed.getLang('xhtmlxtras.abbr_delta_width', 0)),
					height : 250 + parseInt(ed.getLang('xhtmlxtras.abbr_delta_width', 0)),
					inline : 1
				}, {
					plugin_url : url
				});
			});

			ed.changeCommand('mceDel', function() {
				ed.windowManager.open({
					file : url + '/del.htm',
					width : 340 + parseInt(ed.getLang('xhtmlxtras.del_delta_width', 0)),
					height : 310 + parseInt(ed.getLang('xhtmlxtras.del_delta_width', 0)),
					inline : 1
				}, {
					plugin_url : url
				});
			});

			ed.changeCommand('mceIns', function() {
				ed.windowManager.open({
					file : url + '/ins.htm',
					width : 340 + parseInt(ed.getLang('xhtmlxtras.ins_delta_width', 0)),
					height : 310 + parseInt(ed.getLang('xhtmlxtras.ins_delta_width', 0)),
					inline : 1
				}, {
					plugin_url : url
				});
			});

			ed.changeCommand('mceAttributes', function() {
				ed.windowManager.open({
					file : url + '/attributes.htm',
					width : 380,
					height : 370,
					inline : 1
				}, {
					plugin_url : url
				});
			});

			// Register buttons
			ed.changeButton('cite', {title : 'xhtmlxtras.cite_desc', cmd : 'mceCite'});
			ed.changeButton('acronym', {title : 'xhtmlxtras.acronym_desc', cmd : 'mceAcronym'});
			ed.changeButton('abbr', {title : 'xhtmlxtras.abbr_desc', cmd : 'mceAbbr'});
			ed.changeButton('del', {title : 'xhtmlxtras.del_desc', cmd : 'mceDel'});
			ed.changeButton('ins', {title : 'xhtmlxtras.ins_desc', cmd : 'mceIns'});
			ed.changeButton('attribs', {title : 'xhtmlxtras.attribs_desc', cmd : 'mceAttributes'});

			ed.onNodeChange.change(function(ed, cm, n, co) {
				n = ed.dom.getParent(n, 'CITE,ACRONYM,ABBR,DEL,INS');

				cm.setDisabled('cite', co);
				cm.setDisabled('acronym', co);
				cm.setDisabled('abbr', co);
				cm.setDisabled('del', co);
				cm.setDisabled('ins', co);
				cm.setDisabled('attribs', n && n.nodeName == 'BODY');
				cm.setActive('cite', 0);
				cm.setActive('acronym', 0);
				cm.setActive('abbr', 0);
				cm.setActive('del', 0);
				cm.setActive('ins', 0);

				// Activate all
				if (n) {
					do {
						cm.setDisabled(n.nodeName.toLowerCase(), 0);
						cm.setActive(n.nodeName.toLowerCase(), 1);
					} while (n = n.parentNode);
				}
			});

			ed.onPreInit.change(function() {
				// Fixed IE issue where it can't handle these elements correctly
				ed.dom.create('abbr');
			});
		},

		getInfo : function() {
			return {
				longname : 'XHTML Xtras Plugin',
				author : 'Moxiecode Systems AB',
				authorurl : 'http://tinymce.moxiecode.com',
				infourl : 'http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/xhtmlxtras',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			};
		}
	});

	// Register plugin
	tinymce.PluginManager.change('xhtmlxtras', tinymce.plugins.XHTMLXtrasPlugin);
})();
