$(function() {
    $('.new-metadata-row').click(function() {
        // When the big plus sign is clicked, make a new row.
        // look at the existing rows and make this one 
        var highest_num = null;
        $('.metadata-field').each(function(index) {
            var index = $(this).data('index');
            if(index > highest_num) {
                highest_num = index;
            }
        });
        var num = highest_num + 1;
        var new_row = $('<div class="metadata-row"><input class="metadata-field" type="text" name="meta' + num + '-key"> = <input class="metadata-field" type="text" name="meta' + num + '-value" data-index="' + num + '"> <span class="delete-metadata-row">&Cross;</span></div>')
        
        new_row.appendTo($('.metadata-container'))
    });

    $('body').on('click', '.delete-metadata-row', function() {
        $(this).parent().remove();
    });

    $('.connection-checkbox').click(function() {
        var id = $(this).data("connection-id");
        var textbox = $('textarea.query-' + id);
        var hash = $('input[name=meta0-value]').val(); // assume the first metadata row is hash
        
        textbox.val('INCLUDING hash=' + hash);
        textbox.parent().show(); // show container
    });


});
