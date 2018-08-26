function sleep(n) { //n表示的毫秒数
            var start = new Date().getTime();
            while (true) if (new Date().getTime() - start > n) break;
        }
    $(document).ready(function(){
        $('.page').click(function(){
            var searchStr = location.search;
            var old_href = $(this).attr('href').replace('?', '');
            var searchArray = searchStr.split('&');

            if (searchStr == ''){
                searchStr = '?page=1'
            }

            if (searchStr.indexOf('page')>=0){
                searchArray.pop();
            }

            searchArray.push(old_href);
            if (searchArray.length > 1) {
                $(this).attr('href', searchArray.join('&'));
            }

        })
    });


$(document).ready(function () {
            $("#date-popover").popover({html: true, trigger: "manual"});
            $("#date-popover").hide();
            $("#date-popover").click(function (e) {
                $(this).hide();
            });
        
            $("#my-calendar").zabuto_calendar({
                action: function () {
                    return myDateFunction(this.id, false);
                },
                action_nav: function () {
                    return myNavFunction(this.id);
                },
                ajax: {
                    url: "show_data.php?action=1",
                    modal: true
                },
                legend: [
                    {type: "text", label: "Special event", badge: "00"},
                    {type: "block", label: "Regular event", }
                ]
            });
        });
        function myNavFunction(id) {
            $("#date-popover").hide();
            var nav = $("#" + id).data("navigation");
            var to = $("#" + id).data("to");
            console.log('nav ' + nav + ' to: ' + to.month + '/' + to.year);
        }
