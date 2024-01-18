$(".homepage-category-sec").slick({
  slidesToShow: 2,
  slidesToScroll: 1,
  autoplay: true,
  swipeToSlide: true,
  infinite:true,
  variableWidth: true,
  autoplaySpeed: 2000,
  dots: false,
  arrows:false
});
$('.homepage-tranding-bottom-wrap').slick({
  slidesToShow: 3,
  slidesToScroll: 1,
  infinite:true,
  swipeToSlide:true,
  autoplay: true,
  variableWidth: true,
  autoplaySpeed: 2000,
  dots: false,
  arrows:false
});
$('.offcial-partner-bottom').slick({
  slidesToShow: 3,
  slidesToScroll: 1,
  infinite:true,
  swipeToSlide:true,
  autoplay: true,
  variableWidth: true,
  autoplaySpeed: 2000,
  dots: false,
  arrows:false
});
$('.prodcut-sec-slide').slick({
  slidesToShow: 1,
  slidesToScroll: 1,
  infinite:true,
  autoplay: true,
  autoplaySpeed: 2000,
  dots: true,
  arrows:false
});
$('.featured-description').slick({
  slidesToShow: 2,
  slidesToScroll: 1,
  swipeToSlide: true,
  infinite:true,
  autoplay: true,
  variableWidth: true,
  autoplaySpeed: 2000,
  speed:300,
  dots: false,
  arrows:false
});
$('.offcial-partner-home2-featured').slick({
  slidesToShow: 3,
  slidesToScroll: 1,
  swipeToSlide: true,
  infinite:true,
  autoplay: true,
  variableWidth: true,
  autoplaySpeed: 2000,
  dots: false,
  arrows:false
});
$('.home2-inspiration').slick({
  slidesToShow: 2,
  slidesToScroll: 1,
  infinite:true,
  swipeToSlide: true,
  autoplay: true,
  variableWidth: true,
  autoplaySpeed: 2000,
  dots: false,
  arrows:false
});
$('.wallet-payment-slider,.profile-pay-img-sec,.payment-method-checkoutpage-full ').slick({
  slidesToShow: 4.5,
  slidesToScroll: 1,
  swipeToSlide: true,
  infinite: false,
  autoplay: false,
  variableWidth: true,
  autoplaySpeed: 2000,
  speed: 300,
  dots: false,
  arrows:false
});

$('.pay-btn').on('click',function(){
  $(this).toggleClass('active');
});
$('.size-section-deatils').slick({
  slidesToShow: 3.5,
  slidesToScroll: 1,
  swipeToSlide: true,
  infinite: false,
  autoplay: false,
  variableWidth: true,
  autoplaySpeed: 2000,
  speed: 300,
  dots: false,
  arrows:false
});
$('.color-sec').slick({
  slidesToShow: 6.1,
  slidesToScroll: 1,
  swipeToSlide: true,
  infinite: false,
  autoplay: false,
  variableWidth: true,
  autoplaySpeed: 2000,
  speed: 300,
  dots: false,
  arrows:false
});
$('.image-video-sec-full').slick({
  slidesToShow: 3,
  slidesToScroll: 1,
  swipeToSlide: true,
  infinite: true,
  autoplay: true,
  variableWidth: true,
  autoplaySpeed: 2000,
  dots: false,
  arrows:false
});
$(".skip_btn_1").click(function(){

  $("#first").removeClass("active");
  $(".first_slide").removeClass("active");  

  $("#second").addClass("active");
  $(".second_slide").addClass("active");

});

$(".skip_btn_2").click(function(){
 $("#second").removeClass("active");
 $(".second_slide").removeClass("active");

 $("#third").addClass("active");
 $(".third_slide").addClass("active");
});
$('.opt-sec').on('click',function(){
  $(this).toggleClass('active');
}); 
$(document).ready(function() {
  console.log("ready");
  $(".close-btn").click(function(){
    $("#search-input").val(""); 
    console.log('button clicked')
  });
});
$(document).on('click', '.read-more-btn-text', function(){

  if($(this).find('.readless').hasClass("readless")){
    $(this).parent().find('.read-more-text').hide();
    $(this).parent().find('.product2-readmore').removeClass('rotate-icon');
    $(".read-more-btn-text p").text('Read More').removeClass('readless');

  } else {

    $(this).parent().find('.read-more-text').css('display', 'inline-block');
    $(this).parent().find('.read_dots').hide();

    $(this).parent().find('.product2-readmore').addClass('rotate-icon');
    $(".read-more-btn-text p").text('Read Less').addClass('readless');
  }
});
$('.insta_type_wrap div:first').addClass('active');
$('.hero-heading div:first').siblings("div").hide();
$('.hero-heading div:first').show();

$('.insta_type_wrap a').click(function(){

  $('.insta_type_wrap a').removeClass('active');
  $(this).addClass('active');
  $('.hero-heading div:first').hide();
  $('.hero-heading div:first').siblings("div").hide();

  var activeTab = $(this).attr('href');
  $(activeTab).show();
  return false;
}); 
$("#eye").click(function() {
  $(this).toggleClass("fa-eye fa-eye-slash");
  input = $(this).parent().find("input");
  if (input.attr("type") == "password") {
    input.attr("type", "text");
  } else {
    input.attr("type", "password");
  }
});
$("#eye1").click(function() {
  $(this).toggleClass("fa-eye fa-eye-slash");
  input = $(this).parent().find("input");
  if (input.attr("type") == "password") {
    input.attr("type", "text");
  } else {
    input.attr("type", "password");
  }
});
$('.item-bookmark').on('click',function(){
  $(this).toggleClass('active');
}); 
$('.add').on('click', function () {
  if ($(this).prev().val() < 100) {
    $(this).prev().val(+$(this).prev().val() + 1);
  }
});
$('.sub').on('click', function () {
  if ($(this).next().val() > 1) {
    if ($(this).next().val() > 1) $(this).next().val(+$(this).next().val() - 1);
  }
});
var $radioButtons = $('#change-language-page input[type="radio"],#currency-sec input[type="radio"');
$radioButtons.click(function() {
  $radioButtons.each(function() {
    $(this).parent().toggleClass('language-sel', this.checked);
  });
});
$(".payment-mode .check-select-mode input[type='radio']").change(function(){
  var item=$(this);    
  if(item.is(":checked"))
  {
    window.location.href= item.data("target")
  }    
});
$('.otp-box').on('click',function(){
  $(this).addClass('active');
}); 
$(function() {
  var rangePercent = $('range-slider').val();
  $('range-slider').on('change input', function() {
    rangePercent = $('range-slider').val();
    $('.value').text(rangePercent);
  });
});
$('.buy-now-btn a:last-child').hide();
$('.payment-mode-custom input:radio').change(function () {
  if ($('#payment-type1').is(":checked")) {
    $('.buy-now-btn a:first-child').show();
    $('.buy-now-btn a:last-child').hide();
  } else {  
    $('.buy-now-btn a:first-child').hide();
    $('.buy-now-btn a:last-child').show();
  }
});
$(window).scroll(function(){
  if ($(window).scrollTop() >= 20) {
    $('#top-navbar').addClass('fixed');
  }
  else {
    $('#top-navbar').removeClass('fixed');
  }
});
$(window).on("load" , function () {
  $('.loader').fadeOut();
  $('.loader-mask').delay(350).fadeOut('slow');
});