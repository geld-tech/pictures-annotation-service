<template>
  <div class="index">
    <!-- Container -->
    <b-container class="bv-example-row">
        <h2 id="header">Picture Annotation Service</h2>
        <div v-if="loading" class="loading">
            <h6>Loading...</h6>
            <img src="/static/images/spinner.gif" width="32" height="32"/>
        </div>
        <div v-else>
            <b-row align-v="start" align-h="around">
                <b-col sm="12">
                    <div>
                        <b-form-file multiple accept="image/*"
                                ref="files-input"
                                v-model="files" v-bind:state="Boolean(files)"
                                placeholder="Choose files..." drop-placeholder="Drop files here..." browse-text="Browse">
                           <template slot="file-name" slot-scope="{ names }">
                             <b-badge variant="dark">{{ names[0] }}</b-badge>
                             <b-badge v-if="names.length > 1" variant="dark" class="ml-1">+ {{ names.length - 1 }} More files</b-badge>
                           </template>
                        </b-form-file>
                    </div>
                </b-col>
            </b-row>
            <b-row class="my-1">
              <b-col sm="12">
                <div class="float-right">
                  <b-button @click="onReset" class="mr-2">Clear</b-button>
                  <b-button @click="onSubmit">Send</b-button>
                </div>
              </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="12">
                    <div v-if="$store.state.task.status != 'UNDEFINED'">
                        <p><strong>Task</strong> {{ taskId }} ({{ $store.state.task.status }})</p>
                        <p v-if="taskId">
                            <strong>Results</strong>
                            <ul v-if="$store.state.task.status == 'COMPLETE'">
                              <li v-for="(result, index) in $store.state.task.results" v-bind:key="index">
                                <b-img rounded fluid center thumbnail class="image"
                                    v-bind:src="'results/' + result.task_id + '/' + result.filename"
                                    v-bind:alt="result.filename"></b-img>
                                <p>{{ result.identification }}</p>
                              </li>
                            </ul>
                            <span class="error" v-else-if="$store.state.task.status == 'FAILED'">Identification failed..</span>
                        </p>
                    </div>
                    <div v-else>
                        <br />
                    </div>
                </b-col>
            </b-row>
        </div>
    </b-container>
  </div>
</template>

<script>
import { postFiles } from '@/api'

export default {
  name: 'Index',
  props: ['loading', 'data', 'labels'],
  data() {
    return {
      error: '',
      files: [],
      taskId: '',
      taskStatus: '',
      results: ''
    }
  },
  watch: {
    'taskId': function(value) {
        if (value != '') {
          /* Dispatch asynchronous action to Vuex */
          this.$store.dispatch('getStatus', {taskId: value})
            .catch(err => {
              /* Display error message */
              this.error = err.message
            })
        }
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault()
      if (this.files) {
        postFiles(this.files)
          .then(response => {
            this.$refs['files-input'].reset()
            this.taskId = response.task_id
          })
          .catch(err => {
            /* Reset our form values */
            this.error = err.message
          })
        this.$refs['files-input'].reset()
      }
    },
    onReset(evt) {
      evt.preventDefault()
      this.$refs['files-input'].reset()
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
.container {
  max-width: 800px;
  margin:  0 auto;
}
.image {
  height: 160px;
}
.error {
  color: #e43f3f;
  font-weight: bold;
}
</style>
