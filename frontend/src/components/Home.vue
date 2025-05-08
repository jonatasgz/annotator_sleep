<template>
  <div id="app" class="min-vh-100 d-flex flex-column">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary px-3">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Annotator</a>
        <div class="d-flex gap-2">
          <button @click="downloadDB" class="btn btn-outline-light btn-sm">Download DB</button>
          <button class="btn btn-outline-light btn-sm" @click.prevent="downloadPredictions">Download Y</button>
        </div>
      </div>
    </nav>

    <main class="container-fluid flex-grow-1 mt-3">
      <!-- 3-column layout -->
      <div class="row g-4">
        <!-- Left Column: Episode + Forms -->
        <div class="col-lg-3">
          <div class="card shadow-sm mb-2">
            <div class="card-body p-2">
              <h6>Episode Info</h6>
              <form @submit.prevent="getEpisode" class="row g-2">
                <div class="col-12">
                  <label for="patient_id" class="form-label mb-1">Patient ID</label>
                  <input type="text" id="patient_id" v-model="episode.patient_id" class="form-control form-control-sm"
                    required />
                </div>
                <div class="col-12">
                  <label for="episode_date" class="form-label mb-1">Episode Date</label>
                  <input type="date" id="episode_date" v-model="episode.episode_date"
                    class="form-control form-control-sm" required />
                </div>
                <div class="col-12">
                  <button type="submit" class="btn btn-primary btn-sm w-100">Load/Create</button>
                </div>
              </form>
              <div v-if="message" class="alert alert-info mt-2 mb-0 py-1 px-2 small">{{ message }}</div>
            </div>
          </div>

          <div v-if="episodeLoaded" class="card shadow-sm">
            <div class="card-body p-2">

              <div v-show="formPage === 1">
                <div class="mb-2">
                  <label class="form-label mb-1">Gender
                  </label>
                  <div class="d-flex gap-2">
                    <label><input type="radio" value="male" v-model="episode.gender" /> Masculino</label>
                    <label><input type="radio" value="fale" v-model="episode.gender" /> Feminino</label>
                    <label><input type="radio" value="other" v-model="episode.gender" /> Outro</label>
                  </div>
                </div>
                <div class="mb-2">
                  <label class="form-label mb-1 mt-2">Birth Date
                  </label>
                  <input type="date" class="form-control form-control-sm" v-model="episode.birth_date" />
                </div>
                <div class="row g-2">
                  <div class="col">
                    <label class="form-label mb-1 mt-2">Weight
                    </label>
                    <input type="number" class="form-control form-control-sm" v-model="episode.weight" />
                  </div>
                  <div class="col">
                    <label class="form-label mb-1 mt-2">Height
                    </label>
                    <input type="number" class="form-control form-control-sm" v-model="episode.height" />
                  </div>
                </div>
                <div class="mt-1">
                  <label class="form-label mb-1 mt-2">Medication List
                  </label>
                  <textarea class="form-control form-control-sm" rows="2" v-model="episode.medication_list"></textarea>
                </div>
              </div>

              <template v-for="(group, index) in fieldGroups" :key="'form-group-' + index">
                <div v-show="formPage === index + 2">
                  <div v-for="field in group" :key="field" class="mb-2">
                    <label class="form-label text-capitalize mb-1 mt-2">{{ field.replaceAll('_', ' ') }}
                      <span v-if="predictions[field] && showPredict" class="ms-2 badge bg-info text-dark">
                        {{ predictions[field] }}
                      </span>
                    </label>

                    <template v-if="['epworth_scale'].includes(field)">
                      <input type="number" class="form-control form-control-sm" v-model="episode[field]" />
                    </template>

                    <template
                      v-else-if="['suffocation_waking_levels', 'snoring_levels', 'apneas_levels', 'insomnia_levels'].includes(field)">
                      <select class="form-select form-select-sm" v-model="episode[field]">
                        <option disabled value="">Select one</option>
                        <option value="dont know">Doesn't know</option>
                        <option value="never">Never</option>
                        <option value="sometimes">Sometimes</option>
                        <option value="frequent">Frequent</option>
                        <option value="always">Always</option>
                        <option value="missing">Missing</option>
                      </select>
                    </template>

                    <template v-else-if="field === 'tobacco'">
                      <div class="d-flex gap-2">
                        <label><input type="radio" value="yes" v-model="episode[field]" /> Yes</label>
                        <label><input type="radio" value="no" v-model="episode[field]" /> No</label>
                        <label><input type="radio" value="ex" v-model="episode[field]" /> Ex</label>
                        <label><input type="radio" value="missing" v-model="episode[field]" /> Missing</label>
                      </div>
                    </template>

                    <template v-else-if="field === 'alcohol'">
                      <div class="d-flex gap-2">
                        <label><input type="radio" value="yes" v-model="episode[field]" /> Yes</label>
                        <label><input type="radio" value="no" v-model="episode[field]" /> No</label>
                        <label><input type="radio" value="sometimes" v-model="episode[field]" /> Sometimes</label>
                        <label><input type="radio" value="missing" v-model="episode[field]" /> Missing</label>
                      </div>
                    </template>

                    <template
                      v-else-if="['diabetes', 'dyslipidemia', 'arterial_hypertension', 'snoring', 'apneas'].includes(field)">
                      <div class="d-flex gap-2">
                        <label><input type="radio" value="yes" v-model="episode[field]" /> Yes</label>
                        <label><input type="radio" value="no" v-model="episode[field]" /> No</label>
                        <label><input type="radio" value="dont know" v-model="episode[field]" /> Don't know</label>
                        <label><input type="radio" value="missing" v-model="episode[field]" /> Missing</label>
                      </div>
                    </template>

                    <template v-else-if="field === 'complete'">
                      <div class="d-flex gap-2">
                        <label><input type="radio" value="true" v-model="episode.complete" /> Yes</label>
                        <label><input type="radio" value="false" v-model="episode.complete" /> No</label>
                      </div>
                    </template>

                    <template v-else>
                      <div class="d-flex gap-2">
                        <label><input type="radio" value="yes" v-model="episode[field]" /> Yes</label>
                        <label><input type="radio" value="no" v-model="episode[field]" /> No</label>
                        <label><input type="radio" value="missing" v-model="episode[field]" /> Missing</label>
                      </div>
                    </template>
                  </div>
                </div>
              </template>

              <div class="d-flex justify-content-between mt-4">
                <button class="btn btn-sm btn-outline-secondary" :disabled="formPage === 1" @click="formPage--">
                  Previous
                </button>

                <span>Page {{ formPage }} / {{ totalPages }}</span>

                <button v-if="formPage < totalPages" class="btn btn-sm btn-primary" @click="formPage++">
                  Next
                </button>

                <button v-else class="btn btn-sm btn-success" @click="submitForm">
                  Submit
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-2 flex-wrap gap-2">
                <button class="btn btn-primary btn-sm" @click="analyzeText">
                  {{ editText ? 'Analyze' : 'Edit' }}
                </button>

                <!-- Badges on the right -->
                <div class="d-flex align-items-center flex-wrap gap-1">
                  <span v-for="(label, type) in typeLabels" :key="type" class="badge p-2" :style="{
                    backgroundColor: defaultColors[type],
                    color: getContrastColor(defaultColors[type]),
                    fontSize: '0.75rem'
                  }">
                    {{ label }}
                  </span>
                </div>
              </div>

              <div>
                <div v-if="editText">
                  <textarea class="form-control" v-model="inputText" rows="20" style="height: 75vh;"
                    placeholder="Insert text here..."></textarea>
                </div>
                <div v-else>
                  <div class="form-control bg-light overflow-auto" style="height: 75vh; white-space: pre-wrap;"
                    :key="highlightedSegments.length">
                    <template v-for="(segment, index) in highlightedSegments" :key="index">
                      <span v-if="segment.highlight" :style="{
                        backgroundColor: segment.color,
                        color: getContrastColor(segment.color),
                        padding: '3px',
                        borderRadius: '3px'
                      }">
                        {{ segment.text }}
                      </span>
                      <span v-else>{{ segment.text }}</span>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column: Highlights -->
        <div class="col-lg-3">
          <div class="sticky-top" style="top: 1rem">

            <div class="card shadow-sm mb-3">
              <div class="card-body py-2 px-3">
                <div class="form-check form-switch d-flex justify-content-between align-items-center">
                  <label class="form-check-label" for="autoNERtoggle">
                    Automatic recognition
                  </label>
                  <input class="form-check-input" type="checkbox" id="autoNERtoggle" v-model="autoHighlightEnabled"/>
                </div>
              </div>
            </div>

            <div class="card shadow-sm mb-3">
              <div class="card-body py-2 px-3">
                <div class="form-check form-switch d-flex justify-content-between align-items-center">
                  <label class="form-check-label" for="predictionsToggle">
                    Show predictions
                  </label>
                  <input class="form-check-input" type="checkbox" id="predictionsToggle" v-model="showPredict"/>
                </div>
              </div>
            </div>

            <div class="card shadow-sm mb-3">
              <div class="card-body p-3">
                <h6 class="mb-3">Add Manual Highlight</h6>

                <div class="input-group mb-3">
                  <input class="form-control form-control-sm" v-model="newWord" placeholder="Enter expression" />
                </div>

                <div class="d-flex gap-2 align-items-center">
                  <input type="color" class="form-control form-control-color p-1" style="width: 2.5rem; height: 2rem;"
                    v-model="selectedColor" />
                  <select class="form-select form-select-sm" v-model="selectedType">
                    <option value="Diagnostico">Diagnostic</option>
                    <option value="Sintoma">Symptom</option>
                    <option value="Medicamento">Drug</option>
                    <option value="ProcedimentoMedico">Procedure</option>
                    <option value="SinalVital">Vitals</option>
                    <option value="Progresso">Outcome</option>
                  </select>
                  <button class="btn btn-primary btn-sm" style="height: 2rem;" @click="addHighlight">Add</button>
                </div>

              </div>
            </div>


            <!-- Grouped Highlights -->
            <div v-for="(group, type) in groupedHighlights" :key="type" class="mb-3">
              <button class="btn btn-outline-secondary w-100 text-start mb-1" type="button" data-bs-toggle="collapse"
                :data-bs-target="`#collapse-${type}`" aria-expanded="true">
                {{ typeLabels[type] || type }} ({{ group.length }})
              </button>
              <ul :id="`collapse-${type}`" class="list-group collapse">
                <li v-for="(item, index) in group" :key="item.id"
                  class="list-group-item d-flex justify-content-between align-items-center">
                  <span>
                    <span class="badge px-2 py-1 me-2"
                      :style="{ backgroundColor: item.color, color: getContrastColor(item.color) }">
                      {{ item.expression }}
                    </span>
                  </span>
                  <button class="btn btn-sm btn-outline-danger" @click="removeHighlight(highlights.indexOf(item))">
                    ×
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'

const router = useRouter()

const fieldGroups = [
  ['alcohol', 'tobacco', 'diabetes', 'heart_failure', 'depression'],
  ['anxiety', 'bariatric_surgery', 'pacemaker', 'defibrillator', 'arrhythmia'],
  ['arterial_hypertension', 'ischemic_heart', 'cerebrovascular', 'asthma', 'copd'],
  ['dyslipidemia', 'renal_failure', 'thyroid_disease', 'dementia', 'cancer'],
  ['glaucoma', 'ge_reflux', 'epworth_scale', 'suffocation_waking', 'suffocation_waking_levels'],
  ['snoring', 'snoring_levels', 'apneas', 'apneas_levels', 'insomnia'],
  ['insomnia_levels', 'complete']
];

const episodeLoaded = ref(false);
const totalPages = ref(1 + fieldGroups.length);
const editText = ref(true);
const inputText = ref("");
const newWord = ref("");
const typeLabels = {
  Diagnostico: 'Diagnostics',
  Sintoma: 'Symptoms',
  Medicamento: 'Drugs',
  ProcedimentoMedico: 'Procedures',
  SinalVital: 'Vitals',
  Progresso: 'Outcomes'
}
const typeOrder = [
  'Diagnostico',
  'Sintoma',
  'Medicamento',
  'ProcedimentoMedico',
  'SinalVital',
  'Progresso'
]
const defaultColors = {
  Diagnostico: '#FF6B6B',
  Sintoma: '#FFA500',
  Medicamento: '#4CAF50',
  ProcedimentoMedico: '#2196F3',
  SinalVital: '#9C27B0',
  Progresso: '#607D8B',
}
const selectedType = ref("Diagnostico");
const selectedColor = ref(defaultColors[selectedType.value])
const highlights = ref([]);
const namedEnt = ref([]);
const episode = ref({
  patient_id: "",
  episode_date: "",
});
const predictions = ref({})
const message = ref("");
const formPage = ref(1);
const autoHighlightEnabled = ref(true)
const showPredict = ref(true)

onMounted(async () => {
  try {
    const [highlightsRes, configRes] = await Promise.all([
      axios.get("/highlights"),
    ]);
    highlights.value = highlightsRes.data;
  } catch (error) {
    console.error("Failed to load config or highlights:", error);
  }
});

watch(selectedType, (newType) => {
  if (newType && defaultColors[newType]) {
    selectedColor.value = defaultColors[newType]
  }
});

watch(formPage, (newVal) => {
  if (newVal !== 1 && newVal !== totalPages.value) {
    message.value = "";
  }
});

const getEpisode = async () => {
  try {
    const response = await axios.post("/get_episode", episode.value);
    episode.value = response.data.data;
    episodeLoaded.value = true;
    message.value = response.data.message;
    get_predict();
  } catch (error) {
    console.error("Error fetching episode:", error);
    message.value = "Error: Unable to fetch or create episode.";
    episodeLoaded.value = false;
  }
};

const submitForm = async () => {
  try {
    const response = await axios.post("/submit_episode", episode.value);
    console.log("Episode submitted successfully:", response.data);
    message.value = "Episode submitted successfully!";
    episodeLoaded.value = false
    episode.value = ref({
      patient_id: "",
      episode_date: "",
    });
    formPage.value = 1
    inputText.value = ""
    editText.value = true
  } catch (error) {
    console.error("Error submitting episode:", error);
    message.value = "Error: Could not submit the episode.";
  }
};


const highlightedSegments = computed(() => {
  if (!inputText.value) return [];

  const text = inputText.value;
  const segments = [];

  const manualMatches = [];

  highlights.value.forEach(({ expression, color }) => {
    const cleanExpr = expression.trim();
    const regex = new RegExp(escapeRegex(cleanExpr), "gi");

    let match;
    while ((match = regex.exec(text)) !== null) {
      const start = expandToWordStart(text, match.index);
      const end = expandToWordEnd(text, match.index + match[0].length);
      const fullMatch = text.slice(start, end);

      manualMatches.push({
        start,
        end,
        text: fullMatch,
        color,
        type: "Manual"
      });
    }
  });

  const autoMatches = autoHighlightEnabled.value ? nerHighlights.value : [];

  const allMatches = [...manualMatches, ...autoMatches].sort((a, b) => a.start - b.start);

  const nonOverlapping = [];
  let lastEnd = 0;
  for (const m of allMatches) {
    if (m.start >= lastEnd) {
      nonOverlapping.push(m);
      lastEnd = m.end;
    }
  }

  let cursor = 0;
  for (const m of nonOverlapping) {
    if (cursor < m.start) {
      segments.push({ text: text.slice(cursor, m.start), highlight: false });
    }
    segments.push({ text: m.text, highlight: true, color: m.color });
    cursor = m.end;
  }

  if (cursor < text.length) {
    segments.push({ text: text.slice(cursor), highlight: false });
  }

  return segments;
});

function expandToWordStart(text, index) {
  while (index > 0 && /\w/.test(text[index - 1])) {
    index--;
  }
  return index;
}

function expandToWordEnd(text, index) {
  while (index < text.length && /\w/.test(text[index])) {
    index++;
  }
  return index;
}

const addHighlight = async () => {
  if (!newWord.value || !selectedType.value) return;
  try {
    await axios.post("/highlights", {
      expression: newWord.value,
      color: selectedColor.value,
      type: selectedType.value,
    });
    const response = await axios.get("/highlights");
    highlights.value = response.data;
    newWord.value = "";
  } catch (error) {
    console.error("Error adding highlight:", error);
  }
};

const removeHighlight = async (index) => {
  try {
    const highlightId = highlights.value[index].id;
    await axios.delete(`/delete_highlight/${highlightId}/`);
    highlights.value.splice(index, 1);
  } catch (error) {
    console.error("Error deleting highlight:", error);
  }
};

const analyzeText = async () => {
  if (!episodeLoaded.value) {
    message.value = "To analyze the text you first need to load or create an episode";
    return;
  }

  if (editText.value) {
    try {
      const response = await axios.post("/ner", {
        text: inputText.value,
      });
      namedEnt.value = response.data;
      editText.value = false;
    } catch (error) {
      console.error("Error fetching NER:", error);
    }
    await predict();
  } else {
    editText.value = true;
  }
};

const predict = async () => {
  try {
    const response = await axios.post("/predict", {
      text: inputText.value,
      episode: episode.value["id"]
    });
    predictions.value = response.data
  } catch (error) {
    console.error("Couldn't make predictions", error);
  }
}

const get_predict = async () => {
  try {
    const response = await axios.get("/predict", {
      params: {
        episode: episode.value["id"]
      }
    });
    predictions.value = response.data
  } catch (error) {
    console.error("There was an error getting existing prediction data")
  }
}

const nerHighlights = computed(() =>
  namedEnt.value.map((item) => ({
    start: item.start,
    end: item.end,
    text: item.text,
    type: item.type,
    color: defaultColors[item.type]
  }))
);


const getContrastColor = (hex) => {
  const r = parseInt(hex.substring(1, 3), 16);
  const g = parseInt(hex.substring(3, 5), 16);
  const b = parseInt(hex.substring(5, 7), 16);
  const luminance = 0.299 * r + 0.587 * g + 0.114 * b;
  return luminance > 128 ? "#000000" : "#FFFFFF";
};

function escapeRegex(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const groupedHighlights = computed(() => {
  const groups = {};

  highlights.value.forEach((item) => {
    if (!groups[item.type]) groups[item.type] = [];
    groups[item.type].push(item);
  });

  Object.keys(groups).forEach(type => {
    groups[type].sort((a, b) => a.color.localeCompare(b.color));
  });

  const sortedAndLabeled = {};

  typeOrder.forEach(type => {
    if (groups[type]) {
      const label = typeLabels[type] || type;
      sortedAndLabeled[label] = groups[type];
    }
  });
  return sortedAndLabeled;
});

const downloadDB = async () => {
  try {
    const response = await axios.get('/download_db', {
      responseType: 'blob'
    });

    const blob = new Blob([response.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'episodes.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Download failed:', error);
    alert('Could not download CSV. Please try again.');
  }
}

const downloadPredictions = async () => {
  try {
    const response = await axios.get('/download_predictions', {
      responseType: 'blob'
    });

    const blob = new Blob([response.data], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'predictions.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Download failed:', error);
    alert('Could not download CSV. Please try again.');
  }
}

</script>

<style scoped>
textarea {
  resize: vertical;
}
</style>
