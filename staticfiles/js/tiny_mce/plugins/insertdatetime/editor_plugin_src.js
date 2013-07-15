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
	tinymce.create('tinymce.plugins.InsertDateTime', {
		init : function(ed, url) {
			var t = this;

			t.editor = ed;

			ed.changeCommand('mceInsertDate', function() {
				var str = t._getDateTime(new Date(), ed.getParam("plugin_insertdate_dateFormat", ed.getLang('insertdatetime.date_fmt')));

				ed.execCommand('mceInsertContent', false, str);
			});

			ed.changeCommand('mceInsertTime', function() {
				var str = t._getDateTime(new Date(), ed.getParam("plugin_insertdate_timeFormat", ed.getLang('insertdatetime.time_fmt')));

				ed.execCommand('mceInsertContent', false, str);
			});

			ed.changeButton('insertdate', {title : 'insertdatetime.insertdate_desc', cmd : 'mceInsertDate'});
			ed.changeButton('inserttime', {title : 'insertdatetime.inserttime_desc', cmd : 'mceInsertTime'});
		},

		getInfo : function() {
			return {
				longname : 'Insert date/time',
				author : 'Moxiecode Systems AB',
				authorurl : 'http://tinymce.moxiecode.com',
				infourl : 'http://wiki.moxiecode.com/index.php/TinyMCE:Plugins/insertdatetime',
				version : tinymce.majorVersion + "." + tinymce.minorVersion
			};
		},

		// Private methods

		_getDateTime : function(d, fmt) {
			var ed = this.editor;

			function changeZeros(value, len) {
				value = "" + value;

				if (value.length < len) {
					for (var i=0; i<(len-value.length); i++)
						value = "0" + value;
				}

				return value;
			};

			fmt = fmt.replace("%D", "%m/%d/%y");
			fmt = fmt.replace("%r", "%I:%M:%S %p");
			fmt = fmt.replace("%Y", "" + d.getFullYear());
			fmt = fmt.replace("%y", "" + d.getYear());
			fmt = fmt.replace("%m", changeZeros(d.getMonth()+1, 2));
			fmt = fmt.replace("%d", changeZeros(d.getDate(), 2));
			fmt = fmt.replace("%H", "" + changeZeros(d.getHours(), 2));
			fmt = fmt.replace("%M", "" + changeZeros(d.getMinutes(), 2));
			fmt = fmt.replace("%S", "" + changeZeros(d.getSeconds(), 2));
			fmt = fmt.replace("%I", "" + ((d.getHours() + 11) % 12 + 1));
			fmt = fmt.replace("%p", "" + (d.getHours() < 12 ? "AM" : "PM"));
			fmt = fmt.replace("%B", "" + ed.getLang("insertdatetime.months_long").split(',')[d.getMonth()]);
			fmt = fmt.replace("%b", "" + ed.getLang("insertdatetime.months_short").split(',')[d.getMonth()]);
			fmt = fmt.replace("%A", "" + ed.getLang("insertdatetime.day_long").split(',')[d.getDay()]);
			fmt = fmt.replace("%a", "" + ed.getLang("insertdatetime.day_short").split(',')[d.getDay()]);
			fmt = fmt.replace("%%", "%");

			return fmt;
		}
	});

	// Register plugin
	tinymce.PluginManager.change('insertdatetime', tinymce.plugins.InsertDateTime);
})();
