<template>
    <div>
        <h2>Google Analytics</h2>
        <div v-if="ganalyticsIdSet" class="pt-1">
            <p>Analytics UA ID set successfully!</p>
        </div>
        <div v-else>
            <p>Enter the Google Analytics UA ID in the field below, then press Submit</p>
            <b-form @submit="onSubmitGaId" @reset="onResetGaId" id="uaid" v-if="show">
                <b-container fluid>
                  <b-row class="my-1">
                    <b-col sm="5">
                        <label>Google Analytics UA ID</label>
                    </b-col>
                    <b-col sm="7">
                        <b-form-input type="text" v-model="form.uaid" id="uaIdInput" required></b-form-input>
                    </b-col>
                  </b-row>
                  <b-row class="my-1">
                    <b-col sm="12">
                      <b-button type="reset" variant="danger" v-bind:disabled="disableGaIdButtons" id="uaidClearButton">Clear</b-button>
                      <b-button type="submit" variant="primary" v-bind:disabled="disableGaIdButtons" id="uaidAdminButton">Submit</b-button>
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
  name: 'SetupGanalytics',
  props: ['ganalyticsIdSet'],
  data () {
    return {
      form: {
        uaid: ''
      },
      initialUaid: '',
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
    disableGaIdButtons() {
      return (this.form.uaid === '')
    }
  },
  methods: {
    onSubmitGaId(evt) {
      evt.preventDefault()
      var uaid = sanitizeString(this.form.uaid)
      if (uaid !== '') {
        this.error = ''
        /* Trick to reset/clear native browser form validation state */
        this.show = false
        this.$nextTick(() => { this.show = true })
        /* Fetching the data */
        storeGanalytics(uaid)
          .then(() => {
            this.$emit('set-ganalytics-uaid', true)
          })
          .catch(err => {
            /* Reset our form values */
            this.form.uaid = this.initialUaid
            this.error = err.message
          })
      } else {
        this.error = 'GA UA ID cant be empty!'
      }
    },
    onResetGaId(evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.form.uaid = this.initialUaid
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
          this.initialUaid = response.data.ua_id
          this.form.uaid = this.initialUaid
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
