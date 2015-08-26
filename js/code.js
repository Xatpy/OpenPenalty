// GLOBAL
  var g_Teams = [];
  var g_Players = [];
  var g_Ranking = [];


// FUNCITONS

//Parse --> Settings --> Keys
function initParse(){
  var applicationID = "key";
  var javascriptKey = "key";
  Parse.initialize(applicationID, javascriptKey);
}

function fillTeams(results, combosTeams){
  for (var comboTeamIndex = 0; comboTeamIndex < combosTeams.length; ++comboTeamIndex ) {
    var combo = combosTeams[comboTeamIndex];

    for (var i=0; i < g_Teams.length; i++) {
      var option = document.createElement("option");

      option.id = g_Teams[i].id;
      option.value = g_Teams[i].obj.get("Name");
      option.innerHTML = g_Teams[i].obj.get("Name");

      combo.appendChild(option);
    }
  }
}

function executeCallbacks(callbacks) {
  if (callbacks) {
    for (var indexCallback = 0; indexCallback < callbacks.length; ++ indexCallback) {
      var callb = callbacks[indexCallback];
      if (typeof(callb) === "function") {
        callb();
      }
    }
  }
}

function createOptionPlayer(player) {
  var option = document.createElement("option");
  option.id = player.id;
  option.value = player.get("Name");
  option.innerHTML = player.get("Name");
  return option;
}

function getPlayers(teamName, combo, isGoalkeeper){
  combo.innerHTML = "";
  for (var indexTeams = 0; indexTeams < g_Players.length; ++indexTeams) {
    if (teamName === g_Players[indexTeams].team) {
      for (var indexPlayers = 0; indexPlayers < g_Players[indexTeams].playersArr.length; ++indexPlayers) {
        var pos = g_Players[indexTeams].playersArr[indexPlayers].get("Position");
        if ( (isGoalkeeper && pos === "Portero") || (!isGoalkeeper && pos !== "Portero") ){
          var option = createOptionPlayer(g_Players[indexTeams].playersArr[indexPlayers]);
          combo.appendChild(option); 
        }
      }//for indexPlayers
    }// if teamName
  }// for indexteams
}

function loadPlayers(callbacks){
  for (var indexTeam = 0; indexTeam < g_Teams.length; indexTeam++) {
    var Player = Parse.Object.extend("Player");
    var query = new Parse.Query(Player);
    query.equalTo("EquipoID", g_Teams[indexTeam].obj);
    query.find({
      success: function(results) {
        if (results.length > 0) {
          var teamName = getTeamName(results[0].get("EquipoID").id)
          var objTeamPlayers = {
            team: teamName,
            playersArr: [] 
          };
          for (var indexPlayers = 0; indexPlayers < results.length; ++indexPlayers) {
            objTeamPlayers.playersArr.push(results[indexPlayers]);
          }
          g_Players.push(objTeamPlayers);
          
          executeCallbacks(callbacks);
        }
      },
      error: function(error) {
        alert("Error: " + error.code + " " + error.message);
      }
    });
  }
}


function loadTeams(combosTeams, callbacks){
  var Team = Parse.Object.extend("Team");
  var query = new Parse.Query(Team);
  query.ascending("Name");
  query.find({
    success: function(results) {
      for (var i=0; i < results.length; i++) {
        var option = document.createElement("option");
        var objTeam = {"id": results[i].get("Name"), "obj": results[i]};
        g_Teams.push(objTeam);
      }
      if (combosTeams && combosTeams.length > 0) {
        fillTeams(results, combosTeams);        
      }
      loadPlayers(callbacks);
    },
    error: function(error) {
      alert("Error: " + error.code + " " + error.message);
    }
  });
}

function getPlayersOfTeam(indexTeam, combo){
  combo.innerHTML = "";

  for (var indexPlayer = 0; indexPlayer < g_Teams[indexTeam].length; ++ indexPlayer) {
    var option = document.createElement("option");

    option.id = g_Teams[indexTeam].a.id;
    option.value = results[i].get("Name");
    option.innerHTML = results[i].get("Name");

    combo.appendChild(option);
    combo.appendChild(option);
  }

}

//segundo parametro: es un portero
function getPlayersOfTheTeamParse(obj, isGoalkeeper){
  var Player = Parse.Object.extend("Player");
  var query = new Parse.Query(Player);
  query.equalTo("EquipoID", obj);
  if (isGoalkeeper) {
    //restrict to goakeeper
    query.equalTo("Position", "Portero");
  } else {
    query.notEqualTo("Position", "Portero");
  }

  query.find({
    success: function(results) {
      fillPlayers(results, isGoalkeeper);
    },
    error: function(error) {
      alert("Error: " + error.code + " " + error.message);
    }
  });
}

function getIndexOfTeam(name){
  for (var i=0; i < g_Teams.length; ++i) {
    if (g_Teams[i].id === name) {
      return i;
    }
  }
  return -1;
}

function getTeamObject(name){
   for (var i=0; i < g_Teams.length; ++i) {
    if (g_Teams[i].id === name) {
      return g_Teams[i].obj;
    }
  }
  return -1;
}

function getTeamName(obj) {
  for (var i=0; i < g_Teams.length; ++i) {
    if (g_Teams[i].obj.id === obj) {
      return g_Teams[i].obj.get("Name");
    }
  }
  return "";
}

function getPlayerObjFromTeam(teamName, playerName) {
  for (var indexTeams = 0; indexTeams < g_Players.length; ++indexTeams) {
    if (teamName === g_Players[indexTeams].team) {
      for (var indexPlayers = 0; indexPlayers < g_Players[indexTeams].playersArr.length; ++indexPlayers) {
        if ( playerName === g_Players[indexTeams].playersArr[indexPlayers].get("Name") ){
          return g_Players[indexTeams].playersArr[indexPlayers];
        }
      }//for indexPlayers
    }
  }
  return {};
}

function getPlayerNameFromId(playerId) {
  for (var indexTeams = 0; indexTeams < g_Players.length; ++indexTeams) {
    if (playerId === g_Players[indexTeams].team) {
      for (var indexPlayers = 0; indexPlayers < g_Players[indexTeams].playersArr.length; ++indexPlayers) {
        if ( playerId === g_Players[indexTeams].playersArr[indexPlayers].id ){
          debugger
          return g_Players[indexTeams].playersArr[indexPlayers].get("Name");
        }
      }//for indexPlayers
    }
  }
  return {};
}

function createTable(results, table) {    
  for (var i = 0; i < results.length; ++i) {
    var tr = document.createElement('tr');

    var tdLanzador = document.createElement('td');
    var tdPortero = document.createElement('td');
    var tdEstado = document.createElement('td');
    var tdLado_Disparo = document.createElement('td');
    var tdLado_Portero = document.createElement('td');
    var tdFecha = document.createElement('td');
    var tdVideo = document.createElement('td');
    debugger
    var textLanzador = document.createTextNode(results[i].get("LanzadorID").get("Name"));    
    var textPortero = document.createTextNode(results[i].get("PorteroID").get("Name"));
    var textEstado = document.createTextNode(results[i].get("Estado"));
    var textLado_Disparo = document.createTextNode(results[i].get("Lado_disparo"));
    var textLado_Portero = document.createTextNode(results[i].get("Lado_portero"));
    var fechaRes = results[i].get("Fecha");
    if (!fechaRes) {
      fechaRes = "";
    }
    var textFecha = document.createTextNode(fechaRes);
    var videoRes = results[i].get("Video");
    if (!videoRes) {
      videoRes = "";
    }
    var textVideo = document.createTextNode(videoRes);

    tdLanzador.appendChild(textLanzador);
    tdPortero.appendChild(textPortero);
    tdEstado.appendChild(textEstado);
    tdLado_Disparo.appendChild(textLado_Disparo);
    tdLado_Portero.appendChild(textLado_Portero);
    tdFecha.appendChild(textFecha);
    tdVideo.appendChild(textVideo);

    tr.appendChild(tdLanzador);
    tr.appendChild(tdPortero);
    tr.appendChild(tdEstado);
    tr.appendChild(tdLado_Disparo);
    tr.appendChild(tdLado_Portero);
    tr.appendChild(tdFecha);
    tr.appendChild(tdVideo);      

    table.appendChild(tr);
  }
}

function setRankingData(results) {
  for (var i = 0; i < results.length; ++i) {
    g_Ranking;
  }
}

function getPenalties(table) {
  var Penalty = Parse.Object.extend("Penalty");
  var penaltyQuery = new Parse.Query(Penalty);
  penaltyQuery.include("LanzadorID");
  penaltyQuery.include("PorteroID");
  penaltyQuery.find({
    success: function(results) {
      debugger
      //setRankingData(results);
      createTable(results, table);
    },
    error: function(error) {
      alert("Error: " + error.code + " " + error.message);
    }
  });

}

