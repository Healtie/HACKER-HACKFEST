/**** Date Time Picker ****/

$(function(){
  $('.input__item').datepicker({
    dateFormat: 'dd-mm-yy',
    showOtherMonths: true,
    showMonthAfterYear: true,
    changeYear: true,
    changeMonth: true,
    showOn: 'both',
    buttonImage: ('assets/svg/calender.svg'),
    buttonImageOnly: true, 
    showAnim: '', 
    onSelect: function () {
            layer.removeClass('show'); //hide back layer when date selected
        }
  });


  $('#datepicker').datepicker('setDate','today'); // set date as todat



  // custom datepicker 
    var calendar = $('#ui-datepicker-div');

    calendar.before('<div class="datepicker-layer"></div>'); // add back layer

    var layer = $('.datepicker-layer'),
        datepicker = $('.hasDatepicker'),
        date = $('.ui-datepicker-calendar tbody a');

    // back layer show
    datepicker.on('click, focus', function () {
        if (calendar.css('display') == 'block') {
            layer.addClass('show');
        }
    });

    //back layer hide
    $(window).on('click', function (e) {
        if (layer.is(e.target)) {
            layer.removeClass('show');
        } if (calendar.css('display') == 'none') {
            layer.removeClass('show');
        }
    });
});