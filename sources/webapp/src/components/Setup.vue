<template>
  <div class="index">
    <!-- Container -->
    <b-container class="bv-example-row">
        <div v-if="loading" class="loading">
            <h6>Loading...</h6>
            <img src="/static/images/spinner.gif" width="32" height="32"/>
        </div>
        <div v-else>
            <vue-step v-bind:now-step="nowStep" v-bind:step-list="stepList" v-bind:style-type="stepperStyle" v-bind:active-color="stepperColor"></vue-step>
            <div class="text-center steps-container">
                <div v-if="nowStep == 1" class="h-100 d-inline-block pt-5">
                    <setup-first-page></setup-first-page>
                </div>
                <div v-else-if="nowStep == 2" class="h-100 d-inline-block pt-5">
                    <setup-password v-bind:adminPasswordSet="adminPasswordSet" v-on:set-admin-password="adminPasswordSet = $event">
                    </setup-password>
                </div>
                <div v-else-if="nowStep == 3" class="h-100 d-inline-block pt-5">
                    <setup-ganalytics v-bind:ganalyticsIdSet="ganalyticsIdSet" v-on:set-ganalytics-uaid="ganalyticsIdSet = $event">
                    </setup-ganalytics>
                </div>
                <div v-else-if="nowStep == 4" class="h-100 d-inline-block pt-5">
                    <setup-ganalytics v-bind:ganalyticsIdSet="ganalyticsIdSet" v-on:set-ganalytics-uaid="ganalyticsIdSet = $event">
                    </setup-ganalytics>
                </div>
                <div v-else class="h-100 d-inline-block pt-5">
                    <h2>Error</h2>
                    <p>Incorrect setup step</p>
                </div>
            </div>
            <div class="float-right" v-if="ganalyticsIdSet">
              <b-button variant="primary" id="backButton" disabled>Back</b-button>
              <b-button variant="primary" v-on:click="startApplication" id="startButton" autofocus>Start</b-button>
            </div>
            <div class="float-right" v-else>
              <b-button variant="primary" v-on:click="previousStep" v-bind:disabled="nowStep == 1" id="defaultBackButton">Back</b-button>
              <b-button variant="primary"
                v-on:click="nextStep"
                v-bind:disabled="nowStep == stepList.length ||
                    (nowStep > 1 && !adminPasswordSet) ||
                    (nowStep > 2 && !modelSet) ||
                    (nowStep > 3 && !ganalyticsIdSet)"
                id="nextButton" autofocus>Next</b-button>
            </div>
        </div>
    </b-container>
  </div>
</template>

<script>
import vueStep from 'vue-step'
import { deauthenticate } from '@/api'
import SetupFirstPage from '@/components/SetupFirstPage'
import SetupPassword from '@/components/SetupPassword'
import SetupGanalytics from '@/components/SetupGanalytics'

export default {
  name: 'Setup',
  props: ['loading', 'data'],
  components: {
    vueStep,
    'setup-first-page': SetupFirstPage,
    'setup-password': SetupPassword,
    'setup-ganalytics': SetupGanalytics
  },
  data () {
    return {
      nowStep: 1,
      stepList: ['First Setup', 'Admin Password', 'ML Model', 'Google Analytics'],
      stepperStyle: 'style2',
      stepperColor: '#0079FB',
      dismissCountDown: 0,
      adminPasswordSet: false,
      ganalyticsIdSet: false
    }
  },
  created() {
    var firstSetup = window.settings.firstSetup
    if (!firstSetup) {
      this.$router.push({name: 'Index'})
    }
  },
  methods: {
    nextStep() {
      if (this.nowStep < this.stepList.length) {
        this.nowStep += 1
      } else {
        this.nowStep = this.stepList.length
      }
    },
    previousStep() {
      if (this.nowStep > 1) {
        this.nowStep -= 1
      } else {
        this.nowStep = 1
      }
    },
    startApplication() {
      deauthenticate()
        .catch(err => {
          this.error = err.message
          this.dismissCountDown = 6
        })
      this.$router.push('/')
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
.processesTable{
  font-size: 14px;
}
.loading {
  width: 50%;
  margin: 0;
  padding-top: 40px;
  padding-left: 40px;
}
.container {
  max-width: 1200px;
  margin:  0 auto;
}
.steps-container {
  height: 400px;
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
