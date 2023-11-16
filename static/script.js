var current_name = "";
var current_password = "";
var home_password = "";

// sets name to be inputted username
function setName(){
	current_name = document.getElementById("user_name").value;
}
// sets password to be inputted password
function setPassword(){
	current_password = document.getElementById("password").value;
}
// When login button is clicked
$("#loginbutton").on("click", function(){
    let username = $("#user_name").val();
    let password = $("#password").val()
    // console.log(username);
    // console.log(password);
    if (username !== "" && password !== "") {
        // console.log("test1");
        $.ajax({
            url: "http://127.0.0.1:5000/",
            type: "POST",
            data: JSON.stringify({"username" : username, "password" : password}),
            contentType: "application/JSON",
            success: function(response){
                // console.log("test2");
                window.location.href = "http://127.0.0.1:5000/" + response;
            }, 
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
    }
    else{
        console.log('wrong username or password');
    }
});

// Admin creates new user
$("#admin_newuser").on("click", function(){
    let username = $("#add_username").val();
    let name = $("#add_name").val();
    let password = $("#add_password").val();
    let acct_type = $("#add_type").val();
    if (username !== "" && name !== "" && password !== "" && acct_type !== ""){
        $.ajax({
            url: "http://127.0.0.1:5000/admin",
            type: "POST",
            data: JSON.stringify({"username" : username, "name" : name, "password" : password, "type" : acct_type, "post" : "user"}),
            contentType: "application/JSON",
            success: function(response){
                window.location.href = "http://127.0.0.1:5000/admin";
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
    }
});

// Admin Creates new class
$("#admin_newclass").on("click", function(){
    let classname = $("#add_class_name").val();
    let time = $("#add_time").val();
    let capacity = $("#add_capacity").val();
    let curr_students = $("#add_current_students").val();
    let teacher = $("#add_teacher").val();
    if (classname !== "" && time !== "" && capacity !== "" && curr_students !== "" && teacher !== ""){
        $.ajax({
            url: "http://127.0.0.1:5000/admin",
            type: "POST",
            data: JSON.stringify({"classname" : classname, "time" : time, "capacity" : capacity, "enrolled" : curr_students, "teacher" : teacher, "post" : "class"}),
            contentType: "application/JSON",
            success: function(response){
                window.location.href = "http://127.0.0.1:5000/admin";
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
    }
});

// Admin Creates new enrollment
$("#admin_enroll").on("click", function(){
    let classname = $("#enroll_classname").val();
    let username = $("#enroll_username").val()
    let grade = $("#enroll_grade").val()
    if (classname !== "" && username !== "" && grade !== ""){
        $.ajax({
            url: "http://127.0.0.1:5000/admin",
            type: "POST",
            data: JSON.stringify({"classname" : classname, "username" : username, "grade" : grade, "post" : "enrollment"}),
            contentType: "application/JSON",
            success: function(response){
                window.location.href = "http://127.0.0.1:5000/admin";
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
    }
});

// Admin Update a User func
$("#update_user").on("click", function(){
    let orig_username = $("#update_original_user").val()
    let new_username = $("#update_new_user").val()
    let new_name = $("#update_new_name").val()
    let new_password = $("#update_new_password").val()
    let new_acct = $("#update_new_type").val()
    $.ajax({
        url: "http://127.0.0.1:5000/admin",
        type: "PUT",
        data: JSON.stringify({"original_name" : orig_username, "new_username" : new_username, "new_name" : new_name, "new_password" : new_password, "new_acct" : new_acct, "put" : "user"}),
        contentType: "application/JSON",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/admin";
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Update a class func
$("#update_class").on("click", function(){
    let original_class = $("#original_className").val()
    let new_class = $("#new_className").val()
    let new_teacher = $("#new_teacher").val()
    let new_time = $("#new_time").val()
    let new_enrolled = $("#new_enrolled").val()
    let new_capacity = $("#new_capacity").val()
    $.ajax({
        url: "http://127.0.0.1:5000/admin",
        type: "PUT",
        data: JSON.stringify({"original_class" : original_class, "new_class" : new_class, "new_teacher" : new_teacher, "new_time" : new_time, "new_enrolled" : new_enrolled, "new_capacity" : new_capacity, "put" : "class"}),
        contentType: "application/JSON",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/admin";
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Update to users grade
$("#update_grade_button").on("click", function(){
    let name = $("#grade_name").val()
    let course = $("#grade_classname").val()
    let grade = $("#updated_grade").val()
    $.ajax({
        url: "http://127.0.0.1:5000/admin",
        type: "PUT",
        data: JSON.stringify({"name" : name, "course" : course, "grade" : grade, "put" : "grade"}),
        contentType: "application/JSON",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/admin";
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Deletes User
$("#delete_user_button").on("click", function(){
    let name = $("#delete_user").val()
    $.ajax({
        url: "http://127.0.0.1:5000/admin",
        type: "DELETE",
        data: JSON.stringify({"name" : name,  "delete" : "user"}),
        contentType: "application/JSON",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/admin";
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Deletes Class
$("#delete_class_button").on("click", function(){
    let course = $("#delete_class").val()
    $.ajax({
        url: "http://127.0.0.1:5000/admin",
        type: "DELETE",
        data: JSON.stringify({"class" : course,  "delete" : "class"}),
        contentType: "application/JSON",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/admin";
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Un-Enrolls Users from class
$("#unenroll_user").on("click", function(){
    let name = $("#delete_enroll_name").val()
    let course = $("#delete_enroll_class").val()
    $.ajax({
        url: "http://127.0.0.1:5000/admin",
        type: "DELETE",
        data: JSON.stringify({"class" : course,  "name" : name, "delete" : "unenroll"}),
        contentType: "application/JSON",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/admin";
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Admin Logout
$("#logoutAdmin").on("click", function(){
    $.ajax({
        url: "http://127.0.0.1:5000/logout",
        type: "GET",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/" + response;
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Redirect to StudentEdit view
$("#s_edit_classes").on("click", function(){
    $.ajax({
        url: "http://127.0.0.1:5000/student",
        type: "GET",
        success: function(){
            window.location.href = "http://127.0.0.1:5000/student/courses";
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Adding courses in studentEdit.html
$("#s_add_classes").on("click", function(){
    const val = $("#adding_class").val();
    $.ajax({
        url: "http://127.0.0.1:5000/student/courses",
        type: "POST",
        data: JSON.stringify({"class_name": val}),
        contentType: "application/JSON",
        success: function(){
            window.location.href = "http://127.0.0.1:5000/student/courses";
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

function student_class_drop(){
    console.log("Please Contact an Admin to drop the class!");
}

// Student view Logout
$("#logoutStudentView").on("click", function(){
    $.ajax({
        url: "http://127.0.0.1:5000/logout",
        type: "GET",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/" + response;
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Returning to Student View
$("#s_view_classes").on("click", function(){
    $.ajax({
        url: "http://127.0.0.1:5000/student/courses",
        type: "GET",
        success: function(){
            window.location.href = "http://127.0.0.1:5000/student";
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Student edit Logout
$("#logoutStudentEdit").on("click", function(){
    $.ajax({
        url: "http://127.0.0.1:5000/logout",
        type: "GET",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/" + response;
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Teacher editing grades
$("#grade_change").on("click", function(){
    let grade = $("#edit_grade").val();
    let student = $("#student_name").val();
    let course_name = document.getElementById("course_name").innerHTML;
    if(student !== "" && grade !== ""){
        $.ajax({
            url: "http://127.0.0.1:5000/teacher/" + course_name,
            type: "PUT",
            data: JSON.stringify({"name":student, "grade":grade}),
            contentType: "application/JSON",
            success: function(response){
                window.location.href = "http://127.0.0.1:5000/teacher/" + course_name;
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
    }
});

// Teacher View Logout
$("#logoutTeacherView").on("click", function(){
    $.ajax({
        url: "http://127.0.0.1:5000/logout",
        type: "GET",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/" + response;
        }, 
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

// Teacher View - Detail logout button
$("#logoutTeacherDetails").on("click", function(){
    $.ajax({
        url: "http://127.0.0.1:5000/logout",
        type: "GET",
        success: function(response){
            window.location.href = "http://127.0.0.1:5000/" + response;
        }, 
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});
