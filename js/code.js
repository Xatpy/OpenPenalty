// GLOBAL
  var g_Teams = [];
  var g_Players = [];


// FUNCITONS

function initParse(){
  Parse.initialize("clave", "clave");
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
  debugger
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
    /*
    if (isGoalkeeper) {
      //restrict to goakeeper
      query.equalTo("Position", "Portero");
    } else {
      query.notEqualTo("Position", "Portero");
    }
    */
    query.find({
      success: function(results) {
        debugger
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
      fillTeams(results, combosTeams);
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

  /*function getPlayerObject(name){
     for (var i=0; i < g_Teams.length; ++i) {
      if (g_Teams[i].id === name) {
        return g_Teams[i].obj;
      }
    }
    return -1;
  }*/


