jQuery(function($){
	$.datepicker.regional[''] = {
		dateFormat: 'dd/mm/yy', firstDay: 1,
		isRTL: false};
	$.datepicker.setDefaults($.datepicker.regional['']);
});
