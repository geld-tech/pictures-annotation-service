<template>
  <div class="index">
    <!-- Container -->
    <b-container v-if="authenticated">
        <h2>Configuration</h2>
        <b-tabs pills card vertical>
          <b-tab title="Admin Password" id="admin-password-tab" active>
            <div class="component">
                <div class="component">
                    <setup-password v-bind:adminPasswordSet="adminPasswordSet" v-on:set-admin-password="adminPasswordSet = $event">
                    </setup-password>
                </div>
            </div>
          </b-tab>
          <b-tab title="Analytics" id="analytics-tab">
            <div class="component">
                <setup-ganalytics v-bind:ganalyticsIdSet="ganalyticsIdSet" v-on:set-ganalytics-uaid="ganalyticsIdSet = $event">
                </setup-ganalytics>
            </div>
           </b-tab>
        </b-tabs>
    </b-container>
    <b-container class="bv-example-row">
        <div>
            <login v-bind:authenticated="authenticated" v-on:set-authenticated="authenticated = $event">
            </login>
        </div>
    </b-container>
  </div>
</template>

<script>
import Login from '@/components/Login'
import SetupPassword from '@/components/SetupPassword'
import SetupGanalytics from '@/components/SetupGanalytics'

export default {
  name: 'Config',
  components: {
    'login': Login,
    'setup-password': SetupPassword,
    'setup-ganalytics': SetupGanalytics
  },
  data () {
    return {
      authenticated: false,
      adminPasswordSet: false,
      ganalyticsIdSet: false
    }
  }
}
</script>

<style scoped>
h2 {
  font-weight: normal;
}
.component {
  height: 500px;
}
.alerting {
  margin: 0 auto;
  text-align: center;
  display: block;
  line-height: 15px;
}
</style>
