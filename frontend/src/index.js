var m = require("mithril");

var title_text = "Text processing system";

var user_input = "Температура 37.9. Давление высокое - 120 на 80.";

var response_from_server = undefined;

var backend_url = window.location.href;

var server_time = "server_time";

// var backend_url = "localhost:8000/api";
var backend_url = "qwork.sizikov.space/api";
var now_url = "https://" + backend_url + "/now"; // https in prod, locally works only with http
var process_text_url = "https://" + backend_url + "/process_text";
var get_history_url = "https://" + backend_url + "/history";

var is_reloading = false

setInterval(function() { autoloadpage(); }, 5000); // it will call the function autoloadpage() after each 5 seconds.
function autoloadpage() {
  if (!is_reloading) {
    return
  }

  console.log("Sending request to:" + now_url);
  m.request({
    url: now_url,
    method: "GET",
  }).then(function(data) {
    server_time = data.time
  })
}

var process_text = function() {
  console.log(process.env.ENVINROMENT)
  console.log("Sending request to:" + process_text_url);
  m.request({
    method: "POST",
    url: process_text_url,
    body: { text: user_input },
    // headers: { "Access-Control-Allow-Origin": "*" },
  }).then(function(data) {
    response_from_server = data;
  });
};

var MainComponent = {
  view: function() {
    return [
      m("a.centered", {
        href: "#!/history"
      }, "History"),
      // m(
      //   "button",
      //   { onclick: function() { is_reloading = !is_reloading; } },
      //   is_reloading ? "Reloading" : "Not reloading"
      // ),
      // m("p", server_time),
      m("h1.centered", title_text),
      m(
        "div.centered",
        m(
          "textarea[name=UserInput][placeholder=Text to process][cols=40][rows=5]",
          {
            oninput: function(e) {
              user_input = e.target.value;
            },
            value: user_input,
          },
          user_input,
        )
      ),
      m(
        "div.centered",
        m(
          "button.centered",
          {
            onclick: process_text,
          },
          "Check text"
        )
      ),
      response_from_server ? m("h3.centered", "Response from server") : null,
      response_from_server ? m("div.centered", [
        m("h4.centered", "Corresponding: " + response_from_server.is_correspond),
        m("h4.centered", "Temperature: " + response_from_server.temperature),
        m("h4.centered", "Systole pressure: " + response_from_server.systole_pressure),
        m("h4.centered", "Diastole pressure: " + response_from_server.diastole_pressure)
      ]) : null,
    ];
  },
};

var history = []

var load_history = function() {
  console.log("Sending request to:" + get_history_url);
  m.request({
    method: "GET",
    url: get_history_url,
  }).then(function(data) {
    console.log(data);
    history = data;
  });
};

var TextProcessHistory = {
  view: function(){
    return [
      m(
        "div.centered",
        m(
          "button.centered",
          {
            onclick: load_history,
          },
          "Load history"
        )
      ),
      history ? m("div", "Текст | Соответствие | Температура | Давление систол | Давление диастол") : "История отсутствует",
      m("div", history.map(function(result) { return m("p", result.text + " | " + (result.is_corresponding ? "✅" : "❌") + " " + result.temperature + " " + result.systole_pressure + " " + result.diastole_pressure)}))
    ]
  }
}

m.route(document.body, "/history", {
  "/": MainComponent,
  "/history": TextProcessHistory,
})
