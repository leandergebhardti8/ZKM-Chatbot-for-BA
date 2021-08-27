$(function() {
    $("<link/>", {
        rel: "stylesheet",
        type: "text/css",
        href: "https://chatbot8.zkm.de/chatbot/zkm-chatbot-button.css"
     }).appendTo("head");

	/*
        *
        *   LOGIC
        *
        */
    /* Hide bot initially */
    // $('#chatbot').hide();
    $('#bubble').hide();

    /* Click handler OPEN bot */
    $(document).on("click", "#bubble", function() {
        $('#bubble').fadeOut(300, () => {
            $('#chatbot').fadeIn(500);
            $('#chatbot').animate({ height: '812px', opacity: 1 }, 300, function() {});
        });
    });

    /* Click handler CLOSE bot */
    $(document).on("click", "#close-chatbot", function() {
        $('#chatbot').animate({ height: '0', opacity: 0 }, 300, function() {
            console.log('Animation complete');
            $('#chatbot').hide();
            $('#bubble').fadeIn(300);
        });
    });
});
