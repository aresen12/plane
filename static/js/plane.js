function add_new_row(){
    let n_id = app.new_row();
    document.getElementById("main_table").innerHTML += `
     <tr id="row${n_id}">
            <td>${n_id}</td>
            <td><input id="name${n_id}" class="form-control"></td>
            <td><input  id="about${n_id}" class="form-control"></td>
            <td ><input id="pr${n_id}" class="form-control"></td>
        </tr>
    `;
}

function gener_data(){
    let den = 0;
    let data = {"title": document.getElementById("title_plane").value, "rows": {}}
    for (let i = 0; i < app.id_rows.length; i++){
        console.log(document.getElementById(`name${app.id_rows[i]}`), `name${app.id_rows[i]}`)
        data['rows'][`${i + 1}`] = {
            "name": document.getElementById(`name${app.id_rows[i]}`).value,
            "about": document.getElementById(`about${app.id_rows[i]}`).value,
            "pr": document.getElementById(`pr${app.id_rows[i]}`).value
        }
    }
    return data;
}


function add_author_ui(){
    let div = document.getElementById("g_m_d");

    if (div.style.display == "none"){
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
}


function add_author(){
     $.ajax({
    url: '/add_author',
    type: 'POST',
    dataType: 'json',
    contentType:'application/json',
    data: JSON.stringify({"id_pr": app.id, "username": document.getElementById("username").value}),
    success: function(json){
       add_author_ui();
    },
    error: function(err) {
        console.error(err);
    }
});
}


function send_plane(){
    let data = gener_data();
     $.ajax({
    url: '/new_plane',
    type: 'POST',
    dataType: 'json',
    contentType:'application/json',
    data: JSON.stringify(data),
    success: function(json){
        window.location = `/plane/${json["id_plane"]}`;
    },
    error: function(err) {
        console.error(err);
    }
});
}


function send_edit(){
    let data = gener_data();
    data["id_plane"] = app.id;
     $.ajax({
    url: '/edit/plane',
    type: 'POST',
    dataType: 'json',
    contentType:'application/json',
    data: JSON.stringify(data),
    success: function(json){
//        window.location = `/plane/${json["id_plane"]}`;
    },
    error: function(err) {
        console.error(err);
    }
});
}


class App{
    constructor(cont_rows, id_plane=0){
        this.id = id_plane;
        this.cont_rows = cont_rows;
        this.id_rows = [];
        for (let i = 1; i < cont_rows + 1; i++){
            this.id_rows.push(i);
        }
    }

    new_row(){
        if (this.id_rows.length > 0){
            this.id_rows.push(this.id_rows[this.id_rows.length - 1] + 1);
        } else {
            this.id_rows.push(1);
        }
        return this.id_rows[this.id_rows.length - 1];
    }

    delete_row(id_row){
        for (let i = 0; i < this.id_rows.length; i++){
            if (this.id_rows[i] == id_row){
                this.id_rows.splice(i, 1);
                document.getElementById(`row${id_row}`).remove()
                break;
            }
        }


    }

}