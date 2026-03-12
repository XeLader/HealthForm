const dropZone = document.getElementById("drop-zone");
dropZone.innerHTML="Перетащите json файл консультации или кликните здесь."
newNode = document.createElement("input");
newNode.type = "file";
newNode.id ="jsonUpload";
newNode.accept=".json,.txt"
dropZone.appendChild(newNode)

document.getElementById("jsonUpload").addEventListener("change", (e) => {
  handleFileUpload(e.target.files[0]);
  });

dropZone.addEventListener("drop", dropHandler);

window.addEventListener("drop", (e) => {
  if ([...e.dataTransfer.items].some((item) => item.kind === "file")) {
    e.preventDefault();
  }
});

dropZone.addEventListener("dragover", (e) => {
  const fileItems = [...e.dataTransfer.items].filter(
    (item) => item.kind === "file",
  );
  if (fileItems.length > 0) {
    e.preventDefault();
    if (true) {
      e.dataTransfer.dropEffect = "copy";
    } else {
      e.dataTransfer.dropEffect = "none";
    }
  }
});

window.addEventListener("dragover", (e) => {
  const fileItems = [...e.dataTransfer.items].filter(
    (item) => item.kind === "file",
  );
  if (fileItems.length > 0) {
    e.preventDefault();
    if (!dropZone.contains(e.target)) {
      e.dataTransfer.dropEffect = "none";
    }
  }
});


function dropHandler(ev) {
  ev.preventDefault();
  const files = [...ev.dataTransfer.items]
  .map((item) => item.getAsFile())
  .filter((file) => file);
  handleFileUpload(files[0]);
}

function handleFileUpload(file) {
  if (!file) return;

  const reader = new FileReader();

  reader.onload = function (e) {
    try {
      const jsonData = safeParseJson(e.target.result);
      processLLMData(jsonData);
    } catch (err) {
      alert("Invalid JSON file");
      console.error(err);
    }
  };

  reader.readAsText(file);
}

function safeParseJson(rawText) {
  const firstBraceIndex = rawText.indexOf("{");

  if (firstBraceIndex === -1) {
    throw new Error("No JSON object found");
  }

  const cleanJson = rawText.slice(firstBraceIndex);
  JSON.parse(cleanJson);
  return JSON.parse(cleanJson);
}


function markAsLlmFilled(element) {
  element.classList.add("llm-filled");
}

function processLLMData(data) {
  processComplains(data);
  processHeredity(data);
  processAnamnesis(data);
  processDiet(data);
  processInsp(data);
  processAllergies(data);
  processLifestyle(data);
  dropZone.innerHTML = "Файл успешно загружен!";
  dropZone.classList.add("llm-filled");
}

function processComplains(data) {
  const text = data.complaints;
  const field = document.getElementById("id_"+"complaints");
  field.value = text;
  markAsLlmFilled(field);
}

function processAnamnesis(data) {
  const text = data.anamnesis;
  const field = document.getElementById("id_"+"anamnesis");
  field.value = text;
  markAsLlmFilled(field);
}

function processGeneralComment(data) {
  const text = data.general_comment;
  const field = document.getElementById("id_"+"text");
  field.value = text;
  markAsLlmFilled(field);
}

function processCommentDiet(data) {
  const text = data.diet.comment;
  const field = document.getElementById("id_"+"comment_diet");
  field.value = text;
  markAsLlmFilled(field);
}


function processHeredity(data) {
  const YNU = ["U","N","Y"];

  details = data.heredity.cardiovascular.details;
  code = data.heredity.cardiovascular.status;
  radio = document.querySelector(
        `input[name="cardiovascular"][value="${code}"]`
      );
  if (radio) radio.checked = true;
  if (details){
    field = document.getElementById("id_"+"cardiovascular_label");
    field.value = details;
  }

  details = data.heredity.oncological.details;
  code = data.heredity.oncological.status;
  radio = document.querySelector(
        `input[name="oncological"][value="${code}"]`
      );
  if (radio) radio.checked = true;
  if (details){
    field = document.getElementById("id_"+"oncological_label");
    field.value = details;
  }

  details = data.heredity.diabetes.details;
  code = data.heredity.diabetes.status;
  radio = document.querySelector(
        `input[name="diabetes"][value="${code}"]`
      );
  if (radio) radio.checked = true;
  if (details){
    field = document.getElementById("id_"+"diabetes_label");
    field.value = details;
  }


  details = data.heredity.thyroid.details;
  code = data.heredity.thyroid.status;
  radio = document.querySelector(
        `input[name="thyroid"][value="${code}"]`
      );
  if (radio) radio.checked = true;
  if(details){
    field = document.getElementById("id_"+"thyroid_label");
    field.value = details;
  }


  details = data.heredity.autoimmune.details;
  code = data.heredity.autoimmune.status;
  radio = document.querySelector(
        `input[name="autoimmune"][value="${code}"]`
      );
  if (radio) radio.checked = true;
  if (details){
    field = document.getElementById("id_"+"autoimmune_label");
    field.value = details;
  }

  field = document.getElementById("id_"+"heredity_Other");
  text =  data.heredity.other;
  if(text){
    field.value = text;
  }
}

function processDiet(data) {
  const allowedDietCodes = [
    "MEAT",
    "PLANT",
    "VEG",
    "LOWCARB",
    "KET",
    "RAW",
    "OTHER"];
  const allowedSnacksCodes = ["N", "R", "O"];

  code = data.diet.type;

  select = document.getElementById("id_"+"diet");
  if (select)
  {
    if (!allowedDietCodes.includes(code)){
      select.value = "OTHER";
    }
    else {
      select.value = code;
    }
  }

  code = data.diet.type;

  select = document.getElementById("id_"+"snacks");
  if (select)
  {
    if (!allowedDietCodes.includes(code)){
      select.value = "N";
    }
    else {
      select.value = code;
    }
  }

  text = data.diet.meals_per_day;
  field = document.getElementById("id_"+"mealscount");
  field.value = text;

  code = data.diet.preferences.meat;
  field = document.getElementById("id_"+"pref_Meat");
  field.checked = code;

  code = data.diet.preferences.fish;
  field = document.getElementById("id_"+"pref_Fish");
  field.checked = code;

  code = data.diet.preferences.dairy;
  field = document.getElementById("id_"+"pref_Dair");
  field.checked = code;

  code = data.diet.preferences.eggs;
  field = document.getElementById("id_"+"pref_Eggs");
  field.checked = code;

  code = data.diet.preferences.vegetables;
  field = document.getElementById("id_"+"pref_Vegs");
  field.checked = code;

  code = data.diet.preferences.fruits;
  field = document.getElementById("id_"+"pref_Frut");
  field.checked = code;

  code = data.diet.preferences.grains;
  field = document.getElementById("id_"+"pref_Groa");
  field.checked = code;

  code = data.diet.preferences.sweets;
  field = document.getElementById("id_"+"pref_Swet");
  field.checked = code;

  code = data.diet.preferences.fast_food;
  field = document.getElementById("id_"+"pref_Fast");
  field.checked = code;

  code = data.diet.preferences.coffee_drinks;
  field = document.getElementById("id_"+"pref_Cofe");
  field.checked = code;

  code = data.diet.preferences.alcohol;
  field = document.getElementById("id_"+"pref_Alco");
  field.checked = code;

  code = data.diet.intolerances.lactose;
  field = document.getElementById("id_"+"intol_Lact");
  field.checked = code;

  code = data.diet.intolerances.gluten;
  field = document.getElementById("id_"+"intol_Glut");
  field.checked = code;

  code = data.diet.intolerances.nuts;
  field = document.getElementById("id_"+"intol_Nuts");
  field.checked = code;

  code = data.diet.intolerances.seafood;
  field = document.getElementById("id_"+"intol_Sea");
  field.checked = code;

  text = data.diet.intolerances.other;
  field = document.getElementById("id_"+"intol_Other");
  field.value = text;

  text = data.diet.comment;
  field = document.getElementById("id_"+"comment_diet");
  field.value = text;
}

function processInsp(data){
  const allowedLiverCodes = ["NRM", "PRO", "NON"];
  const allowedGeneralCodes = ["SAT", "MOD", "SEV", "NON"];
  const allowedBodyCodes = ["AST", "NRM", "HYP", "NON"];


  const allowedSkinCodes = new Map([
    ["CLN","1"],
    ["DRY","2"],
    ["PAL","3"],
    ["PIG","4"],
    ["JAN","5"],
    ["EDM","6"],
    ["NON","7"]]);

  const allowedLympThyr = new Map([   
    ["NRM","1"],
    ["PAL","2"],
    ["PNF","3"],
    ["PNL","4"],
    ["NON","5"]]);

  const allowedMusc = new Map([
    ["NRM","1"],
    ["PAI","2"],
    ["LMT","3"],
    ["EDE","4"],
    ["NON","5"]]);

const allowedTongue = new Map([
    ["PLQ","1"],
    ["MRK","2"],
    ["GEO","3"],
    ["CLR","4"]]);

  code = data.inspection?.general_condition;
  select = document.getElementById("id_"+"insp_General");
  if (select)
  {
    if (!allowedGeneralCodes.includes(code)){
      select.value = "NON";
    }
    else {
      select.value = code;
    }
  }

  code = data.inspection?.body_type;
  select = document.getElementById("id_"+"insp_Body");
  if (select)
  {
    if (!allowedBodyCodes.includes(code)){
      select.value = "NON";
    }
    else {
      select.value = code;
    }
  }

  code = data.inspection?.liver;
  select = document.getElementById("id_"+"insp_Liver");
  if (select)
  {
    if (!allowedLiverCodes.includes(code)){
      select.value = "NON";
    }
    else {
      select.value = code;
      if (code == "PRO")
      {
        select = document.getElementById("id_"+"insp_Liver_protudes");
        text = data.inspection.liver_protrusion_cm;
        if (text)
        {
          select.value = text;
        }
      }
    }
  }

  if (Array.isArray(data.inspection?.skin)) {
    data.inspection.skin.forEach(code => {
      if (allowedSkinCodes.has(code)){
      const checkbox = document.querySelector(
        `input[name="insp_skin"][value="${allowedSkinCodes.get(code)}"]`
      );
      if (checkbox){
       checkbox.checked = true;};
      }
    });
  }

  if (Array.isArray(data.inspection?.tongue)) {
    data.inspection.tongue.forEach(code => {
      if (allowedTongue.has(code)){
      const checkbox = document.querySelector(
        `input[name="insp_Tongue"][value="${allowedTongue.get(code)}"]`
      );
      if (checkbox) checkbox.checked = true;};
    });
  }

  if (Array.isArray(data.inspection?.lymph_nodes)) {
    data.inspection.lymph_nodes.forEach(code => {
      if (allowedLympThyr.has(code)){
      const checkbox = document.querySelector(
        `input[name="insp_lymph"][value="${allowedLympThyr.get(code)}"]`
      );
      if (checkbox) checkbox.checked = true;};
    });
 }

  if (Array.isArray(data.inspection?.thyroid)) {
    data.inspection.thyroid.forEach(code => {
      if (allowedLympThyr.has(code)){
      const checkbox = document.querySelector(
        `input[name="insp_thyroid"][value="${allowedLympThyr.get(code)}"]`
      );
      if (checkbox) checkbox.checked = true;};
    });
 }

  if (Array.isArray(data.inspection?.musculoskeletal)) {
    data.inspection.musculoskeletal.forEach(code => {
      if (allowedMusc.has(code)){
      const checkbox = document.querySelector(
        `input[name="insp_musculoskeletal"][value="${allowedMusc.get(code)}"]`
      );
      if (checkbox) checkbox.checked = true;};
    });
 }


  text = data.inspection.limbs_description;
  field = document.getElementById("id_"+"insp_Limbs");
  field.value = text;

  text = data.inspection.other;
  field = document.getElementById("id_"+"insp_Other");
  field.value = text;
}

function processAllergies(data)
{
  text = data.allergies.food;
  field = document.getElementById("id_"+"foodAllergy");
  field.value = text;

  text = data.allergies.medicine;
  field = document.getElementById("id_"+"medicineAllergy");
  field.value = text;

  text = data.allergies.seasonal;
  field = document.getElementById("id_"+"seasonalAllergy");
  field.value = text;

  text = data.allergies.contact;
  field = document.getElementById("id_"+"contactAllergy");
  field.value = text;

  text = data.allergies.no_allergy;
  field = document.getElementById("id_"+"noAllergy");
  field.value = text;
}

function processLifestyle(data)
{
  text = data.lifestyle.physical_activity;
  field = document.getElementById("id_"+"life_physAct");
  field.value = text;

  text = data.lifestyle.sleep_mode;
  field = document.getElementById("id_"+"life_sleepMode");
  field.value = text;

  text = data.lifestyle.stress;
  field = document.getElementById("id_"+"life_stress");
  field.value = text;

  text = data.lifestyle.last_antibiotics;
  field = document.getElementById("id_"+"life_antibiotics");
  field.value = text;

  text = data.lifestyle.covid_history;
  field = document.getElementById("id_"+"life_covid");
  field.checked = text;

  text = data.lifestyle.vaccination_date;
  field = document.getElementById("id_"+"life_vaccinationDate");
  field.value = text;
}
