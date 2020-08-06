SiderbarHtmlString = '<div class="card">\n' +
    '        <div onclick="dataSetClick" key="<%= id %>"  class="card-body sidebar_item">\n' +
    '          <div class="card-title"> <%= title %></div>\n' +
    '          <h6 class="card-subtitle mb-2 text-muted"><%= created_at %></h6>\n' +
    '          <p class="card-text"><%= description %></p>\n' +
    '          <a href="#" class="card-link">Delete</a>\n' +
    '          <a href="#" class="card-link">Edit</a>\n' +
    '        </div>'


const loading = '<h1>Loading</h1>'

class ChartView {
    renderChart(){
        const cApi  = new CalculatorApi("http://localhost:8081/api/calculator/")
        cApi.getAll().then((response)=>{

            const data  = JSON.parse(response)
            console.log(data)
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

            }
        })
    }
}

function dataSetClick(e){
    const key = e.target.key
    console.log(key)
}


$(document).ready(()=>{
     $('.sidebar_item').click(()=>{
        console.log($(this).data('key'))
    })
})


const newSidebarItemView = new SidebarItemView('').renderSidebar()


const newChart = new ChartView().renderChart()