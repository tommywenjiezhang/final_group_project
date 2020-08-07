SiderbarHtmlString = '<div class="card" key="<%= id %>" >\n' +
    '        <div onclick="dataSetClick" class="card-body sidebar_item">\n' +
    '          <div class="card-title"> <%= title %></div>\n' +
    '          <h6 class="card-subtitle mb-2 text-muted"><%= created_at %></h6>\n' +
    '          <p class="card-text"><%= description %></p>\n' +
    '          <a href="#" class="card-link">Delete</a>\n' +
    '          <a href="#" class="card-link">Edit</a>\n' +
    '        </div>'


const loading = '<h1>Loading</h1>'


class ChartView {
    constructor(ctx,id) {
        this.api = new CalculatorApi("http://localhost:8081/api/calculator/")
        this.ctx = ctx
        this.id = id
    }

    renderBarChart(){
        this.api.getById(this.id).then((response)=>{
            console.log(response)
            $("#chart_title").text(response.title)
            $("#chart_description_box").text(response.description);
            $("#chart_create_date").text(new Date(response.created_at).toLocaleDateString())
            var myChart = new Chart(this.ctx, {
            type: 'bar',
                data: {
                labels: [...Array(response.values.length-1).keys()].map(val => 'column' + (val +1)),
        datasets: [{
            label: response.title,
            data: response.values.sort(),
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        title: response.title,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});
        })
    }
    renderLineChart(){
        this.api.getById(this.id).then((response) => {
             $("#chart_title").text(response.title)
            $("#chart_description_box").text(response.description);
                  $("#chart_create_date").text(new Date(response.created_at).toLocaleDateString())
             var lineChart = new Chart(this.ctx, {
                 type:'line',
                 data:{
                     labels: [...Array(response.values.length-1).keys()].map(val => 'column' + (val +1)),
                     datasets:[{
                         label: response.title,
                         backgroundColor: '#2a9d8f',
                         data: response.values,
                         borderWidth:1
                     }]
                 },
                   options: {
                        title: response.title,
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero: true
                                }
                            }]
                        }
                    }

             })
        })
    }
    renderPieChart(){
        this.api.getById(this.id).then((response) => {
             $("#chart_title").text(response.title)
            $("#chart_description_box").text(response.description);
             $("#chart_create_date").text(new Date(response.created_at).toLocaleDateString())
             var pieChart = new Chart(this.ctx, {
                 type: 'doughnut',
                 data:{
                     labels: [...Array(response.values.length-1).keys()].map(val => 'column' + (val +1)),
                     datasets:[{
                         label: response.title,
                         backgroundColor: colorSchemeGenerator(response.values.length),
                         data: response.values,
                         borderWidth:1
                     }]
                 },
                   options: {
                        title: response.title
                    }

             })
        })
    }
}


class StatsDataView{
    constructor(id) {
        this.api = new CalculatorApi("http://localhost:8081/api/calculator/")
        this.id = id
    }

    renderDataset(){
         this.api.getById(this.id).then((response) => {
             const {mean,median, mode, stdev, variance} = response.calculation
             console.log({mean,median, mode, stdev, variance} )
             $("#mean").text(mean)
             $("#median").text(median)
             $("#mode").text(mode)
             $('#stdev').text(stdev)
             $('#variance').text(variance)
         })
    }

}

const sideBarIterater  = (dataset) =>{
    const {id,created_at,title,description} = dataset
    const complie = _.template(SiderbarHtmlString)
    $('#datasetList').append(complie({id,created_at,title,description}))
}

class SidebarItemView {
    constructor(html) {
        this.layout = html
    }
    renderSidebar(){
        const cApi  = new CalculatorApi("http://localhost:8081/api/calculator/")
        cApi.getAll().then((response)=>{
            const data = JSON.parse(response)
            if(data.length < 1){
                 $('#datasetList').append(loading)
            }
            else{
                console.log(data)
                _.each(data, sideBarIterater)
                $('#datasetList').on("click", ".card", function(data){
                    const datasetELem = $(this)
                    const canvas = document.getElementById("myChart")
                      const newChart = new ChartView(canvas, parseInt($(this).attr('key'))).renderBarChart()
                    const newDataset = new StatsDataView(parseInt($(this).attr('key'))).renderDataset()
                })
            }
        })
    }

}

function dataSetClick(e){
    const key = e.target.key
    console.log(key)
}



function colorSchemeGenerator(number){
    const colorArray =  shuffle(['1a535c', 'ff6b6b', 'f7fff7', '4ecdc4', '1a535c', 'ff9f1c']).map(val => '#' + val)
    const newColorScheme = []
    var j = 0;
    for(var i=0; i< number; i ++){
        j = i
        var color = colorArray[j]
        if(i > colorArray.length){
            j = 0
        }
        newColorScheme.push(color)
    }
    return newColorScheme
}

function shuffle(a) {
    var j, x, i;
    for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
    }
    return a;
}

$(document).ready(()=>{
        canvas = document.getElementById("myChart")
        ctx =  canvas.getContext("2d")
            ctx.font = "20px Arial"
        ctx .fillText("" +
            "Please select your chart type", 10, 50);
    $("#bar_chart").click(function(){
        const newChart = new ChartView(canvas,1).renderBarChart()
        $(this).children().toggleClass('active')
        const newDataset = new StatsDataView(1).renderDataset()
    })


    $("#line_chart").click(function(){
        const newChart = new ChartView(canvas, 1).renderLineChart()
        $(this).addClass('active')
         $("#bar_chart").children().toggleClass('active')
    })

    $("#pie_chart").click(function(){
        const newChart = new ChartView(canvas, 1).renderPieChart()
        $(this).toggleClass('active')
         $("#bar_chart").children().toggleClass('active')
    })
})


const newSidebarItemView = new SidebarItemView('').renderSidebar()



