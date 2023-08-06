let date;
let dateType
let selectDate
getDateString = date =>`${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`
const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];



window.onload = (event) =>{
    dateType = new Date();
    date = getDateString(dateType)
    console.log(dateType);
    // clearDaylist()
    setDayList(date)
}




function clearDaylist(){
    document.querySelectorAll(".day").forEach(i=>i.remove())
    document.querySelectorAll(".task").forEach(i=>i.remove())
}
async function setDayList(s) {
    clearDaylist()
    let thismonth = new Date(dateType.getFullYear(),dateType.getMonth(),1)
    // i.setDate(1)
    let i = parseInt(thismonth.getDay())
    console.log("this month"+i);
    let n = await eel.getDayList(s)();
    const container = document.getElementById("dividing_day-event")
    c=document.getElementById("calendar")
    n[0].forEach(element =>{
        const newDay = document.createElement("div")
        newDay.classList = `${element[1]}`
        newDay.innerText=`${element[0]}`
        newDay.id=element[2]
        newDay.setAttribute("onclick","addEvent(this)")
        newDay.onmouseup ="document.getElementById('Event_name').select()"
        // console.log(element[3]);
        c.insertBefore(newDay,container)
    });
    document.getElementById("year").textContent = dateType.getFullYear()
    document.getElementById("month").textContent = monthNames[dateType.getMonth()]
    n[1].forEach(element=>{
        dateEvent = new Date(element[2]);
        // dateEvent.setMonth(dateEvent.getMonth()+1)
        // console.log(dateEvent);
        // console.log(element[2]);
        const newEvent = document.createElement('section')
        newEvent.innerText=`${element[1]}`
        newEvent.className = "task task--primary"
        newEvent.setAttribute("onclick",'detailEvent(this)')
        newEvent.style.gridColumn = `${dateEvent.getDay()+1} / span 1`
        newEvent.style.gridRow = Math.floor((i+6+dateEvent.getDate())/7)+1
        newEvent.id = element[0]
        // newEvent.id = Math.floor((i+dateEvent.getDate()))
        console.log(i+'\t'+dateEvent.getDate());
        if(element[4]!='NULL'){
            const detail = document.createElement('div');
            detail.className = "task__detail"
            detail.innerHTML = `<h1>${element[1]}</h1><p>${element[4]}</p>`
            newEvent.appendChild(detail)
        }
        insertAfter(container,newEvent)
    })
}

let idUpdateRef
function detailEvent(a){
    idUpdateRef = a.id
    text = a.innerText.split(/\r\n|\n\r|\n|\r/)
    eventName = text[0]
    event_detail = ""
    if(text.length==4){
        event_detail = text[3]
    }
    console.log(eventName,event_detail);
    document.getElementById("overlay").id = "overlayed"
    obj = document.getElementById("detail")
    obj.className = "shoe"
    obj = obj.getElementsByTagName("form")[0]
    obj.event_name.value = eventName
    obj.event_detail.value = event_detail
}

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}
function getWeekOfMonth(date) {
    let adjustedDate = date.getDate()+date.getDay();
    let prefixes = ['0', '1', '2', '3', '4', '5'];
    return (parseInt(prefixes[0 | adjustedDate / 7])+2);
}




btn = document.getElementById("btn")
btn.addEventListener("click",()=>{
    console.log(date);
    setDayList(date)
});

btn = document.getElementById("btn2")
btn.addEventListener("click",clearDaylist)




function menu(){
    
    document.getElementById("option").className='show'
    document.getElementById("overlay").id = 'overlayed'
    // eel.printtext("a.innerText");
}

function x(){
    console.log("cls");
    document.getElementById("option").className = "nonshow"
    document.getElementById("overlayed").id ='overlay'
    document.getElementById('addbox').className = "nonshow"
    document.getElementById('detail').className =  "nonshow"
}

function selectedM(a){
    dateType.setMonth(monthNames.indexOf(a.innerText))
    dateType.setDate(1)
    date = getDateString(dateType)
    console.log(date);
    document.getElementById("smonthActive").id="smonth"
    a.id = "smonthActive"
    setDayList(date)
    x()
}
function selectedY(a){
    dateType.setFullYear(parseInt(a.innerText))    
    dateType.setDate(1)
    date = getDateString(dateType)
    console.log(date);    
    document.getElementById("syearActive").id="syear"
    a.id = "syearActive"
    setDayList(date)
    x()
}

function addEvent(a){
    if(!!a.id){
        id = a.id.slice(1,11)
        selectDate = id
        // eel.printtext("\t\t\t\tAdd Event : "+id)
        document.getElementById('addbox').className = "show"
        document.getElementById('addinto').innerText = "Add Event to "+id
        document.getElementById("overlay").id = "overlayed"
        setTimeout(()=>{
            document.getElementById('event_detail').value = ""
            title =document.getElementById('Event_name')
            this.value = ""
            title.focus()
            title.select()
        },100)
    }
}

function submitEvent(a){
    form = a.parentNode.parentNode;

    eventNamme = form.event_name.value
    eventDetail = form.event_detail.value

    eel.printtext("\t\t\t\tAdd Event : "+selectDate)
    eel.upload(eventNamme,selectDate,eventDetail)
    setDayList(date)
    x()
}

function submitEventUpdate(a){
    form = a.parentNode.parentNode;

    eventNamme = form.event_name.value
    eventDetail = form.event_detail.value

    console.log(idUpdateRef);
    eel.updateEvent(idUpdateRef,eventNamme,selectDate,eventDetail)
    setDayList(date)
    x()
}

function deleteSelectedEvent(){
    eel.deleteByID(idUpdateRef)
    setDayList(date)
    x()
}