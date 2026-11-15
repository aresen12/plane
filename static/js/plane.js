var cont_rows = 1;

function add_new_row(){
    document.getElementById("main_table").innerHTML += `
     <tr id="row${cont_rows + 1}">
            <td>${cont_rows + 1}</td>
            <td><input id="name${cont_rows + 1}" class="form-control"></td>
            <td><input  id="about${cont_rows + 1}" class="form-control"></td>
            <td ><input id="pr${cont_rows + 1}" class="form-control"></td>
        </tr>
    `;
    globalThis.cont_rows++;
}

function send_plane(){
    let data = {"title": document.getElementById("title_plane").value, "rows": {}}
    for (let i = 1; i <= cont_rows; i++){
        console.log(document.getElementById(`name${i}`), `name${i}`)
        data['rows'][`${i}`] = {
            "name": document.getElementById(`name${i}`).value,
            "about": document.getElementById(`about${i}`).value,
            "pr": document.getElementById(`pr${i}`).value
        }
    }
    console.log(data)
     $.ajax({
    url: '/new_plane',
    type: 'POST',
    dataType: 'json',
    contentType:'application/json',
    data: JSON.stringify(data),
    success: function(json){
//        window.location = "/plane"
    },
    error: function(err) {
        console.error(err);
    }
});
}