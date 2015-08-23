// GLOBAL
  var g_Teams = [];
  var g_Players = [];


// FUNCITONS

function initParse(){
  Parse.initialize("CLAVE_APP, CLAVE_JAVASCRIPT")
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

function loadPlayers(){
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

      executeCallbacks(callbacks);        

      loadPlayers();
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


