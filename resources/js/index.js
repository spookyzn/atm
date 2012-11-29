function getQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)","i");
    var r = window.location.search.substr(1).match(reg);
    if (r!=null)
        return unescape(r[2]);
    return null;
}

Ext.onReady(function() {
    var chart_store = Ext.create('Ext.data.JsonStore', {
        sotreId: 'chartStore',
        autoLoad: true,
        fields: ['date', 'focus', 'comment'],
        proxy: {
            type: 'ajax',
            url: '/json/daily_count/',
            extraParams: {
                'startDate': getQueryString('startDate'),
                'endDate': getQueryString('endDate')
            }
        }
    });


    //var store = Ext.create('Ext.data.JsonStore', {"fields": ["date", "focus", "comment"], "data": [{"date": "2012-11-01", "comment": 19387, "focus": 0}, {"date": "2012-11-02", "comment": 16413, "focus": 0}, {"date": "2012-11-03", "comment": 5564, "focus": 0}, {"date": "2012-11-04", "comment": 5420, "focus": 0}, {"date": "2012-11-05", "comment": 17809, "focus": 0}, {"date": "2012-11-06", "comment": 16561, "focus": 0}, {"date": "2012-11-07", "comment": 16575, "focus": 0}, {"date": "2012-11-08", "comment": 14786, "focus": 3777705}]} );

    var lineChart = Ext.create('Ext.chart.Chart',{
        style: 'background:#fff',
        animate: true,
        store: chart_store,
        shadow: true,
        axes: [{
            type: 'Numeric',
            minimum: 0,
            position: 'left',
            fields: ['comment', 'focus'],
            title: 'heat of stock',
            minorTickSteps: 1
        }, {
            type: 'Category',
            position: 'bottom',
            fields: ['date'],
            title: 'Date'
        }],
        series: [{
            type: 'line',
            highlight: {
                size: 7,
                radius:7
            },
            tips: {
                trackMouse: true,
                width: 220,
                height: 28,
                renderer: function(storeItem, item) {
                    this.setTitle(storeItem.get('date') + ': ' + storeItem.get('comment') + ' comments');
                }
            },
            axis: 'left',
            xField: 'date',
            yField: 'comment'
        },{
            type: 'line',
            highlight: {
                size: 7,
                radius:7
            },
            tips: {
                trackMouse: true,
                width: 200,
                height: 28,
                renderer: function(storeItem, item) {
                    this.setTitle(storeItem.get('date') + ': ' + storeItem.get('focus') + ' focus');
                }
            },
            axis: 'left',
            xField: 'date',
            yField: 'focus'
        }],
        legend: {
            position: 'right'
        }
    });


    Ext.create('Ext.panel.Panel', {
            layout: 'fit',
            collapsible: true,
            title: 'Test panel',
            width: 800,
            height: 200,
            renderTo: Ext.getBody(),
            items: [lineChart]
        }
    );


    /*
    Ext.create('Ext.window.Window', {
        title: 'test',
        width: 500,
        height:300,
        layout: 'fit',
        items: [lineChart]
    }).show();
    */
});