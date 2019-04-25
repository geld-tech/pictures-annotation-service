<template>
  <div class="index">
    <!-- Container -->
    <b-container class="bv-example-row">
        <div v-if="authenticated" class="pt-1">
          <b-container fluid>
            <b-row class="my-1">
              <b-col sm="10" class="float-right">
                  <b-button @click="onSubmitLogout" type="button" variant="primary" id="adminLogoutButton">Logout</b-button>
              </b-col>
            </b-row>
          </b-container>
        </div>
        <div v-else class="pt-1">
            <h2 id="loginHeader">Login</h2>
            <p>Enter the system administration password in the following input field, then Submit</p>
            <b-form @submit="onSubmitPassword" @reset="onResetPassword" id="adminPasswordForm" v-if="show">
                <b-container fluid>
                  <b-row class="my-1">
                    <b-col sm="5">
                        <label>Password</label>
                    </b-col>
                    <b-col sm="7">
                        <b-form-input type="password" autocomplete="current-password" v-model="form.adminPassword" id="adminPassword" aria-label="adminPassword" required></b-form-input>
                    </b-col>
                  </b-row>
                  <b-row class="my-1">
                    <b-col sm="10" class="float-right">
                        <b-button type="reset" variant="danger" v-bind:disabled="disableAdminResetButton" id="adminResetButton">Clear</b-button>
                        <b-button type="submit" variant="primary" v-bind:disabled="disableAdminSubmitButton" id="adminSubmitButton">Submit</b-button>
                    </b-col>
                  </b-row>
                  <b-row class="my-1">
                    <b-col md="6" offset-md="3">
                       <!-- Alerting -->
                       <div class="alerting">
                         <b-alert :show="dismissCountDown" dismissible variant="danger" @dismissed="error=''" @dismiss-count-down="countDownChanged">
                           <p>{{ error }}</p>
                         </b-alert>
                       </div>
                    </b-col>
                  </b-row>
                </b-container>
            </b-form>
        </div>
    </b-container>
  </div>
</template>

<script>
import { authenticate, deauthenticate } from '@/api'
import { sanitizeString } from '@/tools/utils'

export default {
  name: 'Login',
  data () {
    return {
      form: {
        adminPassword: ''
      },
      authenticated: false,
      error: '',
      show: true
    }
  },
  computed: {
    disableResetButton() {
      return (this.form.adminPassword === '')
    },
    disableSubmitButton() {
      return (this.form.adminPassword === '')
    }
  },
  methods: {
    onSubmitLogout() {
      deauthenticate()
        .catch(err => {
          this.error = err.message
          this.dismissCountDown = 6
        })
      this.authenticated = false
      this.$emit('set-authenticated', false)
    },
    onSubmitPassword(evt) {
      evt.preventDefault()
      var password = sanitizeString(this.form.adminPassword)
      this.form.adminPassword = ''
      this.dismissCountDown = 0
      this.error = ''
      if (password !== '') {
        /* Trick to reset/clear native browser form validation state */
        this.show = false
        this.$nextTick(() => { this.show = true })
        /* Fetching the data */
        authenticate(password)
          .then(() => {
            this.authenticated = true
            this.$emit('set-authenticated', true)
          })
          .catch(err => {
            this.error = err.message
            this.dismissCountDown = 6
          })
      } else {
        this.error = 'Authentication failed!'
        this.dismissCountDown = 6
      }
    },
    countDownChanged (dismissCountDown) {
      this.dismissCountDown = dismissCountDown
    },
    onResetPassword(evt) {
      evt.preventDefault()
      /* Reset our form values */
      this.form.adminPassword = ''
      /* Trick to reset/clear native browser form validation state */
      this.show = false
      this.$nextTick(() => { this.show = true })
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
