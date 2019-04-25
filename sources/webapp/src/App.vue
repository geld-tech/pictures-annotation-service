<template>
  <div id="app">
    <!-- Navigation -->
    <b-navbar class="navbar-expand-lg navbar-light bg-white fixed-top" toggleable>
        <b-navbar-nav>
          <b-navbar-brand href="/"><img src="/static/images/geld.tech_32x32.png" width="30" height="30" alt="" /> __PACKAGE_NAME__</b-navbar-brand>
        </b-navbar-nav>
    </b-navbar>
    <!-- Alerting -->
    <div class="alerting col-md-4 col-md-offset-4">
      <b-alert :show="dismissCountDown" dismissible variant="danger" @dismissed="error=''" @dismiss-count-down="countDownChanged">
        <p>{{ error }}</p>
      </b-alert>
    </div>
    <!-- Container -->
    <div id="app-container">
        <router-view
            v-bind:data="data"
            v-bind:loading="loading"
            v-bind:labels="labels">
        </router-view>
    </div>
  </div>
</template>

<script>
import { fetchData } from '@/api'

export default {
  name: 'App',
  data() {
    return {
      data: {},
      labels: [],
      dismissCountDown: 0,
      error: '',
      loading: false,
      refreshInterval: 0,
      show: true
    }
  },
  created() {
    var firstSetup = window.settings.firstSetup
    if (firstSetup) {
      this.$router.push('/Setup')
    } else {
      this.loading = false
      /* Trick to reset/clear native browser form validation state */
      this.data = {}
      this.labels = []
      this.show = false
      this.$nextTick(() => { this.show = true })
      /* Fetching the data */
      this.loading = true
      this.fetchResourcesData()
      /* Sets interval for auto-refresh */
      this.refreshInterval = window.setInterval(this.fetchResourcesData, 15000)
      }
  },
  beforeDestroy() {
    window.clearInterval(this.refreshInterval)
  },
  methods: {
    fetchResourcesData() {
      this.loading = true
      fetchData()
        .then(response => {
          this.data = response.data
          this.labels = response.labels
          this.loading = false
        })
        .catch(err => {
          this.error = err.message
          this.loading = false
        })
    },
    countDownChanged (dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 30px;
  padding-top: 50px;
  margin-bottom: 10px;
  padding-bottom: 20px;
}
@media screen and (min-width: 601px) {
  #app {
    margin-top: 5px;
    padding-top: 70px;
    font-size: 1.3em;
  }
}
@media screen and (max-width: 600px) {
  #app {
    margin-top: 15px;
    margin-bottom: 10px;
    padding-top: 170px;
    font-size: 1em;
  }
}
.alerting {
  margin: 0 auto;
  text-align: center;
  display: block;
  line-height: 15px;
}
.loading {
  width: 50%;
  margin: 0;
  padding-top: 40px;
  padding-left: 40px;
}
.list-no-bullet {
  padding: 0;
  margin: 0;
  list-style-type: none;
}
</style>
