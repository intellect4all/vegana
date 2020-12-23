$(".banner-part").slick({
  dots: true,
  fade: true,
  infinite: true,
  autoplay: true,
  arrows: true,
  speed: 1000,
  prevArrow: '<i class="fas fa-long-arrow-alt-right dandik"></i>',
  nextArrow: '<i class="fas fa-long-arrow-alt-left bamdik"></i>',
  slidesToShow: 1,
  slidesToScroll: 1,
  responsive: [
    { breakpoint: 1199, settings: { slidesToShow: 1, slidesToScroll: 1 } },
    { breakpoint: 991, settings: { slidesToShow: 1, slidesToScroll: 1 } },
    { breakpoint: 767, settings: { slidesToShow: 1, slidesToScroll: 1 } },
    {
      breakpoint: 576,
      settings: { slidesToShow: 1, slidesToScroll: 1, arrows: false },
    },
  ],
});
$(".product-slider").slick({
  dots: false,
  infinite: true,
  autoplay: false,
  arrows: true,
  speed: 1000,
  prevArrow: '<i class="fas fa-long-arrow-alt-right dandik"></i>',
  nextArrow: '<i class="fas fa-long-arrow-alt-left bamdik"></i>',
  slidesToShow: 4,
  slidesToScroll: 4,
  responsive: [
    { breakpoint: 1199, settings: { slidesToShow: 4, slidesToScroll: 4 } },
    { breakpoint: 991, settings: { slidesToShow: 3, slidesToScroll: 3 } },
    { breakpoint: 767, settings: { slidesToShow: 2, slidesToScroll: 2 } },
    {
      breakpoint: 576,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        variableWidth: true,
        arrows: false,
      },
    },
  ],
});
$(".blog-slider").slick({
  dots: false,
  infinite: true,
  autoplay: false,
  arrows: true,
  speed: 1000,
  prevArrow: '<i class="fas fa-long-arrow-alt-right dandik"></i>',
  nextArrow: '<i class="fas fa-long-arrow-alt-left bamdik"></i>',
  slidesToShow: 2,
  slidesToScroll: 2,
  responsive: [
    { breakpoint: 1199, settings: { slidesToShow: 2, slidesToScroll: 2 } },
    { breakpoint: 991, settings: { slidesToShow: 1, slidesToScroll: 1 } },
    {
      breakpoint: 767,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        variableWidth: true,
        arrows: true,
      },
    },
    {
      breakpoint: 576,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        variableWidth: true,
        arrows: false,
      },
    },
  ],
});
$(".blogdet-slider").slick({
  dots: false,
  infinite: true,
  autoplay: false,
  arrows: true,
  speed: 1000,
  prevArrow: '<i class="fas fa-long-arrow-alt-right dandik"></i>',
  nextArrow: '<i class="fas fa-long-arrow-alt-left bamdik"></i>',
  slidesToShow: 3,
  slidesToScroll: 1,
  responsive: [
    { breakpoint: 1199, settings: { slidesToShow: 2, slidesToScroll: 2 } },
    { breakpoint: 991, settings: { slidesToShow: 1, slidesToScroll: 1 } },
    {
      breakpoint: 767,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        variableWidth: true,
        arrows: true,
      },
    },
    {
      breakpoint: 576,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        variableWidth: true,
        arrows: false,
      },
    },
  ],
});
$(".theme-slider").slick({
  dots: false,
  infinite: true,
  autoplay: true,
  arrows: true,
  speed: 1000,
  prevArrow: '<i class="fas fa-long-arrow-alt-right dandik"></i>',
  nextArrow: '<i class="fas fa-long-arrow-alt-left bamdik"></i>',
  slidesToShow: 2,
  slidesToScroll: 1,
  responsive: [
    { breakpoint: 1199, settings: { slidesToShow: 2, slidesToScroll: 2 } },
    { breakpoint: 991, settings: { slidesToShow: 2, slidesToScroll: 1 } },
    { breakpoint: 767, settings: { slidesToShow: 1, slidesToScroll: 1 } },
    {
      breakpoint: 576,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
        variableWidth: true,
        arrows: false,
      },
    },
  ],
});
