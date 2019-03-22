$.ajax({
    url: "/login",
    type: "POST",
    data: { arr },
    success: (res) => {
      if (res.status == 200) {
        localStorage.setItem("token", res.token);
        console.log("success");
      }
    },
    error: (err) => { console.log(err) }
  });