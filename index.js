let countloads = 0;

let fullresponse = "";

let collapsed = false;

function xmlhttpPost(strURL) {
  var xmlHttpReq = false;
  var self = this;
  if (window.XMLHttpRequest) {
    // Mozilla/Safari
    self.xmlHttpReq = new XMLHttpRequest();
  } else if (window.ActiveXObject) {
    // IE
    self.xmlHttpReq = new ActiveXObject("Microsoft.XMLHTTP");
  }
  self.xmlHttpReq.open("POST", strURL, true);
  self.xmlHttpReq.setRequestHeader(
    "Content-Type",
    "application/x-www-form-urlencoded"
  );
  self.xmlHttpReq.onreadystatechange = function () {
    if (self.xmlHttpReq.readyState == 4) {
      $(".list-content").html("");
      countloads = 0;
      fullresponse = self.xmlHttpReq.responseText;
      splitresponse();
    }
  };

  var params = getstandardargs().concat(getquerystring());
  var strData = params.join("&");
  self.xmlHttpReq.send(strData);
}

function getstandardargs() {
  var params = [
    "wt=json",
    "indent=on",
    "fl=url,subjects,description,author,title",
    "json.limit=500",
    "df=all",
  ];

  return params;
}

function clearFilter() {
  $("#inlineRadio1")[0].checked = false;
  $("#inlineRadio2")[0].checked = false;
  $("#inlineRadio3")[0].checked = false;
}

function getquerystring() {
  var query = $("#query").val();
  if (query == "") query = "*.*";

  if ($("#inlineRadio2")[0].checked) query = "subjects:" + query;
  if ($("#inlineRadio1")[0].checked) query = "title:" + query;
  if ($("#inlineRadio3")[0].checked) query = "author:" + query;

  qstr = "q=" + escape(query);
  return qstr;
}

function splitresponse() {
  let ret = [];
  let json = JSON.parse(fullresponse);

  let upper = Math.min(json["response"]["docs"].length, (countloads + 1) * 50);

  for (i = 0; i < upper; i++) {
    ret.push(json["response"]["docs"][i]);
  }
  countloads++;
  updatepage(ret);
}

// this function does all the work of parsing the solr response and updating the page
function updatepage(arr) {
  var html = '<table style="width: 98%;" class="table table-dark mt-3">';
  html += `<caption class="m-2">${arr.length} results</caption>`;
  html += `<tr>
            <th>Title</th>
            <th>Author(s)</th>
            <th>Description</th>
            <th>Subjects</th>
            <th>URL</th>
            </tr>`;
  for (let i = 0; i < arr.length; i++) {
    var doc = arr[i];
    if (doc == undefined) continue;
    html += "<tr>";
    html += `<td class="text-light">${doc.title}</td>`;
    html += `<td class="text-light">${doc.author || "N/A"}</td>`;
    html += `<td class="text-light">${doc.description || "N/A"}</td>`;
    html += `<td class="text-light">${doc.subjects.join(", ")}</td>`;
    html += `<td class="text-light"><a href="${doc.url}" target="_blank">Original</a></td>`;
    html += "</tr>";
  }
  html += "</table>";
  if (
    JSON.parse(fullresponse)["response"]["docs"].length >
    (countloads + 1) * 50
  )
    html +=
      '<div class="w-100 d-flex align-items-center justify-content-center"><button type="button" class="btn btn-light mb-4" onclick="splitresponse()">Load More</button></div>';

  $("#result").html(html);
}

function filterresults() {

  collapsed=false;

  $(".list-content").html("");

  var occurencies = {};
  let ret = [];
  let json = JSON.parse(fullresponse);

  let upper = Math.min(json["response"]["docs"].length, (countloads + 1) * 50);

  for (i = 0; i < upper; i++) {
    element = json["response"]["docs"][i]["subjects"].join(", ");
    Array.isArray(occurencies[element.toLowerCase()])
      ? occurencies[element.toLowerCase()].push(json["response"]["docs"][i])
      : (occurencies[element.toLowerCase()] = Array(
          json["response"]["docs"][i]
        ));

  }

  for (key in occurencies) {
    if (occurencies[key].length > 0) {
      $(".list-content").append(
        '<table class="' +
          key.replace(/[^a-zA-Z0-9]/g, "") +
          ' collapsible table table-dark mt-3">' +
          "<tr><th colspan='5'>" + occurencies[key][0].subjects.join(', ') + "</th></tr>"
      );
      occurencies[key].forEach((element) => {
        $("." + key.replace(/[^a-zA-Z0-9]/g, "")).append(
          '<tr class="content">' +
            `<td>${element["title"]}</td>` +
            `<td>${element.author || "N/A"}</td>` +
            `<td>${element.description || "N/A"}</td>` +
            `<td>${element.subjects.join(', ')}</td>` +
            `<td><a href="${element.url}" target="_blank">Original</a></td>` +
            "</tr>"
        );
      });
      $(".list-content").append("</table>");
      $("#result").html("");
    }
  }

  let coll = $(".collapsible");
  for (let i = 0; i < coll.length; i++) {
    coll.eq(i).click(() => {
      coll
        .eq(i)
        .children()
        .eq(0)
        .children(".content")
        .get()
        .forEach((element) => {
          if (element.style.display != "none") {
            element.style.display = "none";
          } else {
            element.style.display = "table-row";
          }
        });
    });
  }
}

function collapseAll() {
  let coll = $(".collapsible");
  for (let i = 0; i < coll.length; i++) {
    coll.eq(i).children()
    .eq(0)
    .children(".content")
    .get()
    .forEach((element) => {
      console.log(collapsed)
      if (!collapsed){
           element.style.display = "none";
      }
      else {
          element.style.display = "table-row";
        }
    });
  }
  collapsed ^= true;
}
