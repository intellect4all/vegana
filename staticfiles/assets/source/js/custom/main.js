$(document).ready(function () {
  var url = window.location.href;
  url = url.substring(
    0,
    url.indexOf("#") == -1 ? url.length : url.indexOf("#")
  );
  url = url.substring(
    0,
    url.indexOf("?") == -1 ? url.length : url.indexOf("?")
  );
  url = url.substr(url.lastIndexOf("/") + 1);
  if (url == "") {
    url = "index.html";
  }
  $(".navbar-item").each(function () {
    var href = $(this).find("a").attr("href");
    if (url == href) {
      $(this).addClass("active");
    }
  });
});
$(window).on("scroll", function () {
  var scrolling = $(this).scrollTop();
  if (scrolling > 300) {
    $(".navbar-part").addClass("navbar-fixed");
  } else {
    $(".navbar-part").removeClass("navbar-fixed");
  }
});
$(".cart-icon").on("click", function () {
  $(".cart-popup").addClass("active");
  $(".cross-btn").on("click", function () {
    $(".cart-popup").removeClass("active");
  });
});
$(".wish-icon").on("click", function () {
  $(".wish-popup").addClass("active");
  $(".cross-btn").on("click", function () {
    $(".wish-popup").removeClass("active");
  });
});
$(".menu-bar").on("click", function () {
  $(".navbar-slide").addClass("active");
  $(".cross-btn").on("click", function () {
    $(".navbar-slide").removeClass("active");
  });
});
$(function () {
  $(".navbar-dropdown a").click(function () {
    $(this).next().toggle();
    if ($(".dropdown-list:visible").length > 1) {
      $(".dropdown-list:visible").hide();
      $(this).next().show();
    }
  });
});
$(".grid-hori").on("click", function () {
  $(".grid-hori").addClass("active");
  $(".grid-verti").removeClass("active");
  $(".grid-verti").on("click", function () {
    $(".grid-verti").addClass("active");
    $(".grid-hori").removeClass("active");
  });
});
$(function () {
  $(".nasted-dropdown a").click(function () {
    $(this).next().toggle();
    if ($(".nasted-dropdown li ul:visible").length > 1) {
      $(".nasted-dropdown li ul:visible").hide();
      $(this).next().show();
    }
  });
});
$(".eye").on("click", function () {
  $(".eye").toggleClass("fa-eye-slash");
  $(".eye").toggleClass("fa-eye");
  var input = $("#pass");
  if (input.attr("type") === "password") {
    input.attr("type", "text");
  } else {
    input.attr("type", "password");
  }
});
