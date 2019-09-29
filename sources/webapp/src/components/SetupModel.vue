<template>
    <div>
        <h2>Deep Learning Model</h2>
        <div v-if="modelFilename" class="pt-1">
            <p>Model successfully configured!</p>
        </div>
        <div v-else>
            <p>Enter the filename of the model to use the field below, then press Submit</p>
            <b-form @submit="onSubmitModel" @reset="onResetModel" id="filename" v-if="show">
                <b-container fluid>
                  <b-row class="my-1">
                    <b-col sm="5">
                        <label>Filename</label>
                    </b-col>
                    <b-col sm="7">
                        <b-form-input type="text" v-model="form.filename" id="filenameInput" required></b-form-input>
                    </b-col>
                  </b-row>
                  <b-row class="my-1">
                    <b-col sm="12">
                      <b-button type="reset" variant="danger" v-bind:disabled="disableButtons" id="filenameClearButton">Clear</b-button>
                      <b-button type="submit" variant="primary" v-bind:disabled="disableButtons" id="filenameAdminButton">Submit</b-button>
                    </b-col>
                  </b-row>
                </b-container>
            </b-form>
        </div>
    </div>
</template>

<script>
import { getConfig, storeGanalytics } from '@/api'
import { sanitizeString } from '@/tools/utils'

export default {
  name: 'SetupModel',
  props: ['modelFilename'],
  data () {
    return {
      form: {
        filename: ''
      },
      initialFilename: 'model.h5',
      error: '',
      loading: false,
      show: true
    }
  },
  mounted() {
    var firstSetup = window.settings.firstSetup
    if (!firstSetup) {
      this.getGanalyticsConfig()
    }
  },
  computed: {
    disableButtons() {
      return (this.form.filename === '')
    }
  },
  methods: {
    onSubmitModel(evt) {
      evt.preventDefault()
      var filename = sanitizeString(this.form.filename)
      if (filename !== '') {
        this.error = ''
        /* Trick to reset/clear native browser form validation state */
        this.show = false
        this.$nextTick(() => { this.show = true })
        /* Fetching the data */
        storeGanalytics(filename)
          .then(() => {
            this.$emit('set-ganalytics-filename', true)
          })
          .catch(err => {
            /* Reset our form values */
            this.form.filename = this.initialFilename
            this.error = err.message
          })
      } else {
        this.error = 'GA UA ID cant be empty!'
      }
    },
    onResetModel(evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.form.filename = this.initialFilename
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
    },
    getGanalyticsConfig() {
      this.loading = false
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
      /* Fetching the data */
      this.loading = true
      getConfig()
        .then(response => {
          this.initialFilename = response.data.model_filename
          this.form.filename = this.initialFilename
          this.loading = false
        })
        .catch(err => {
          this.error = err.message
          this.loading = false
        })
    }
  }
}
</script>

<style scoped>
h2 {
  font-weight: normal;
}
.container {
  max-width: 1200px;
  margin:  0 auto;
}
.alerting {
  margin: 0 auto;
  text-align: center;
  display: block;
  line-height: 15px;
}
button{
  margin: 1px;
}
</style>
