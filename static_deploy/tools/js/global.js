$(slider_estateagent());

function slider_estateagent() {
    selectedRentOrSale = $('input[name=rent_or_sale]:checked').val();
    selectedRentOrSale = selectedRentOrSale || $('input[name=rent_or_sale]').val();
    $( "#slider-range" ).slider({
      range: true,
      min: 0,
      max: selectedRentOrSale == "rent" ? 10000 : 5000000, // Max property price from database?
      values: selectedRentOrSale == "rent" ? [ 0, 2000 ] : [ 0, 250000],
      slide: function( event, ui ) {
        $( "#amount" ).val( "£" + ui.values[ 0 ] + " - £" + ui.values[ 1 ] );
      }
    });
    $( "#amount" ).val( "£" + $( "#slider-range" ).slider( "values", 0 ) +
      " - £" + $( "#slider-range" ).slider( "values", 1 ) );

};

//When radio buttons are changed, update slider
$('[name="rent_or_sale"]').change(slider_estateagent);
