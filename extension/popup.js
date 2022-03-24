
document.addEventListener('DOMContentLoaded', function() {


    function download(filename, text) {
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);
    
        element.style.display = 'none';
        document.body.appendChild(element);
    
        element.click();
    
        document.body.removeChild(element);
    }
    

    //getting page stuff
      const submitbutton1 = document.getElementById("submitbutton1");
      const submitbutton2 = document.getElementById("submitbutton2");
      const submitbutton3 = document.getElementById("submitbutton3");
      const progressbar = document.getElementById('progressbar');
      const progressbarrow = document.getElementById('progressbarrow');
      const progress = document.getElementById('progress');
      const slowloadrow = document.getElementById('slowload');

      //Getting all the information the user has entered on the page
    const api_key = document.getElementById("api");
    const timezone = document.getElementById("timezone");
    const university = document.getElementById("university");
    const classrange = document.getElementById("classrange");

// writing function for sending api request

//var serverhost = 'http://127.0.0.1:5000/';
var serverhost = 'https://canvashelper.pythonanywhere.com/'

      submitbutton1.onclick = () => {
        

        
        var server_data = [
            {"api": api_key.value,
            "timezone": timezone.value,
            "college": university.value,
            "numcourses": classrange.value,
            "button": "ical"}
        ];

        $.ajax(
            {
                type: "POST",
                url: serverhost,
                data: JSON.stringify(server_data),
                contentType: "application/json",
                dataType: "json",
                error: function(errorThrown) {

                    var probalert = document.getElementById('problemalert');
                    if (probalert == null) {

                        var probalert = document.createElement("div");
                        probalert.setAttribute('class','alert alert-danger alert-dismissible show fade');
                        probalert.setAttribute('id','problemalert');
                        probalert.innerHTML = 'Something went wrong on our end. Try again later.';
                        var dismissbutton = document.createElement("button");
                        dismissbutton.setAttribute('class','btn-close');
                        dismissbutton.setAttribute('type','button');
                        dismissbutton.setAttribute('data-bs-dismiss','alert');
                        dismissbutton.setAttribute('aria-label','Close');
                        probalert.appendChild(dismissbutton);
                        var box = document.getElementById('alertgoeshere');
                        box.appendChild(probalert);
    

                    }
                    else {
                        probalert.innerHTML = 'Something went wrong on our end. Try again later.' + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';

                    }



                },
                success: function(result) {

                    var worked = result['worked'];
                    var file = result['result'];
                    var username = result['username'];

                    if (worked) {
                        var file_name = username + '.ics';
                        download(file_name,file);
                    }
                   else {

                    if (progress.style.display == 'flex') {
                        progress.style.display = 'none';
                    }


                        var probalert = document.getElementById('problemalert');
                        if (probalert == null) {

                            var probalert = document.createElement("div");
                            probalert.setAttribute('class','alert alert-danger alert-dismissible show fade');
                            probalert.setAttribute('id','problemalert');
                            probalert.innerHTML = file;
                            var dismissbutton = document.createElement("button");
                            dismissbutton.setAttribute('class','btn-close');
                            dismissbutton.setAttribute('type','button');
                            dismissbutton.setAttribute('data-bs-dismiss','alert');
                            dismissbutton.setAttribute('aria-label','Close');
                            probalert.appendChild(dismissbutton);
                            var box = document.getElementById('alertgoeshere');
                            box.appendChild(probalert);
        

                        }
                        else {
                            probalert.innerHTML = file + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';

                        }

                
                             }


                }
            }
        );        

        slowloadrow.innerHTML = ""
       
        if (progress.style.display == 'none') {
            progress.style.display = 'flex';
        }
      
        setTimeout(() => {  
        progressbar.style.width = '0%';
        progressbar.style.backgroundColor = '#826AED';

     }, .1);

     setTimeout(() => {  

         for (let i=0;i<100.001;i += 0.001) {
     progressbar.style.width = i.toString() + '%';
     }

    }, 400);
      
      }
               
      submitbutton2.onclick = () => {


        var server_data = [
            {"api": api_key.value,
            "timezone": timezone.value,
            "college": university.value,
            "numcourses": classrange.value,
            "button": "todolist"}
        ];

        $.ajax(
            {
                type: "POST",
                url: serverhost,
                data: JSON.stringify(server_data),
                contentType: "application/json",
                dataType: "json",
                error: function(errorThrown) {

                    var probalert = document.getElementById('problemalert');
                    if (probalert == null) {

                        var probalert = document.createElement("div");
                        probalert.setAttribute('class','alert alert-danger alert-dismissible show fade');
                        probalert.setAttribute('id','problemalert');
                        probalert.innerHTML = 'Something went wrong on our end. Try again later.';
                        var dismissbutton = document.createElement("button");
                        dismissbutton.setAttribute('class','btn-close');
                        dismissbutton.setAttribute('type','button');
                        dismissbutton.setAttribute('data-bs-dismiss','alert');
                        dismissbutton.setAttribute('aria-label','Close');
                        probalert.appendChild(dismissbutton);
                        var box = document.getElementById('alertgoeshere');
                        box.appendChild(probalert);
    

                    }
                    else {
                        probalert.innerHTML = 'Something went wrong on our end. Try again later.' + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';

                    }



                },

                success: function(result) {

                    var worked = result['worked'];
                    var file = result['result'];
                    var username = result['username'];

                    if (worked) {
                        var file_name = username + '.csv';
                        download(file_name,file);
                    }
                   else {

                    if (progress.style.display == 'flex') {
                        progress.style.display = 'none';
                    }

                        var probalert = document.getElementById('problemalert');
                        if (probalert == null) {

                            var probalert = document.createElement("div");
                            probalert.setAttribute('class','alert alert-danger alert-dismissible show fade');
                            probalert.setAttribute('id','problemalert');
                            probalert.innerHTML = file;
                            var dismissbutton = document.createElement("button");
                            dismissbutton.setAttribute('class','btn-close');
                            dismissbutton.setAttribute('type','button');
                            dismissbutton.setAttribute('data-bs-dismiss','alert');
                            dismissbutton.setAttribute('aria-label','Close');
                            probalert.appendChild(dismissbutton);
                            var box = document.getElementById('alertgoeshere');
                            box.appendChild(probalert);
        

                        }
                        else {
                            probalert.innerHTML = file + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';

                        }

                
                             }


                }
            }
        );        

        slowloadrow.innerHTML = ""
       
       if (progress.style.display == 'none') {
           progress.style.display = 'flex';
       }
     
       setTimeout(() => {  
        progressbar.style.width = '0%';
        progressbar.style.backgroundColor = '#C879FF';

     }, .1);

     setTimeout(() => {  

         for (let i=0;i<100.001;i += 0.001) {
     progressbar.style.width = i.toString() + '%';
     }

    }, 400);

     
     }

     submitbutton3.onclick = () => {
       
        var server_data = [
            {"api": api_key.value,
            "timezone": timezone.value,
            "college": university.value,
            "numcourses": classrange.value,
            "button": "studybuddy"}
        ];

        $.ajax(
            {
                type: "POST",
                url: serverhost,
                data: JSON.stringify(server_data),
                contentType: "application/json",
                dataType: "json",
                error: function(errorThrown) {

                    var probalert = document.getElementById('problemalert');
                    if (probalert == null) {

                        var probalert = document.createElement("div");
                        probalert.setAttribute('class','alert alert-danger alert-dismissible show fade');
                        probalert.setAttribute('id','problemalert');
                        probalert.innerHTML = 'Something went wrong on our end. Try again later.';
                        var dismissbutton = document.createElement("button");
                        dismissbutton.setAttribute('class','btn-close');
                        dismissbutton.setAttribute('type','button');
                        dismissbutton.setAttribute('data-bs-dismiss','alert');
                        dismissbutton.setAttribute('aria-label','Close');
                        probalert.appendChild(dismissbutton);
                        var box = document.getElementById('alertgoeshere');
                        box.appendChild(probalert);
    

                    }
                    else {
                        probalert.innerHTML = 'Something went wrong on our end. Try again later.' + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';

                    }



                },

                success: function(result) {

                    var worked = result['worked'];
                    var file = result['result'];
                    var username = result['username'];

                    if (worked) {
                        var file_name = username + ' Study Buddies.csv';
                        download(file_name,file);
                    }
                   else {

                    if (progress.style.display == 'flex') {
                        progress.style.display = 'none';
                    }
             
                        var probalert = document.getElementById('problemalert');
                        if (probalert == null) {

                            var probalert = document.createElement("div");
                            probalert.setAttribute('class','alert alert-danger alert-dismissible show fade');
                            probalert.setAttribute('id','problemalert');
                            probalert.innerHTML = file;
                            var dismissbutton = document.createElement("button");
                            dismissbutton.setAttribute('class','btn-close');
                            dismissbutton.setAttribute('type','button');
                            dismissbutton.setAttribute('data-bs-dismiss','alert');
                            dismissbutton.setAttribute('aria-label','Close');
                            probalert.appendChild(dismissbutton);
                            var box = document.getElementById('alertgoeshere');
                            box.appendChild(probalert);
        

                        }
                        else {
                            probalert.innerHTML = file + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';

                        }

                
                             }


                }
            }
        );        


       if (progress.style.display == 'none') {
           progress.style.display = 'flex';
       }
     
       setTimeout(() => {  
       progressbar.style.width = '0%';
       progressbar.style.backgroundColor = '#FFB7FF';

    }, .1);

    setTimeout(() => {  
        for (let i=0;i<100.001;i += 0.001) {
    progressbar.style.width = i.toString() + '%';

    }
    
   }, 400);
   

   setTimeout(() => {  
    slowloadrow.innerHTML = "";
   }, 5000);

     }



 });
