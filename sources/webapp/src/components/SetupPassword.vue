<template>
    <div>
        <h2>Admin Password</h2>
        <div v-if="adminPasswordSet" class="pt-1">
            <p>Password set successfully!</p>
        </div>
        <div v-else>
            <p>Enter the system administration password in the following input field, then Submit</p>
            <b-form @submit="onSubmitPassword" @reset="onResetPassword" id="adminPasswordForm" v-if="show">
                <b-container fluid>
                  <b-row class="my-1">
                    <b-col sm="5">
                        <label>Password</label>
                    </b-col>
                    <b-col sm="7">
                        <b-form-input type="password" autocomplete="new-password" v-model="form.adminPassword" id="adminPassword" aria-label="adminPassword" required>
                        </b-form-input>
                    </b-col>
                    <b-col sm="5">
                        <label>Password (repeat)</label>
                    </b-col>
                    <b-col sm="7">
                        <b-form-input type="password" autocomplete="new-password" v-model="form.adminPasswordRepeat" id="adminPasswordRepeat" aria-label="adminPasswordRepeat" required>
                        </b-form-input>
                    </b-col>
                  </b-row>
                  <b-row class="my-1">
                    <b-col sm="10">
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
    </div>
</template>

<script>
import { storeAdminPassword } from '@/api'
import { sanitizeString } from '@/tools/utils'

export default {
  name: 'SetupPassword',
  props: ['adminPasswordSet'],
  data () {
    return {
      form: {
        adminPassword: '',
        adminPasswordRepeat: ''
      },
      error: '',
      show: true
    }
  },
  computed: {
    disableAdminResetButton() {
      return (this.form.adminPassword === '' && this.form.adminPasswordRepeat === '')
    },
    disableAdminSubmitButton() {
      return (this.form.adminPassword === '' || this.form.adminPasswordRepeat === '' || this.form.adminPassword !== this.form.adminPasswordRepeat)
    }
  },
  methods: {
    onSubmitPassword(evt) {
      evt.preventDefault()
      var password = sanitizeString(this.form.adminPassword)
      var passwordRepeat = sanitizeString(this.form.adminPasswordRepeat)
      this.form.adminPassword = ''
      this.form.adminPasswordRepeat = ''
      this.dismissCountDown = 0
      this.error = ''
      if (password !== '' && password === passwordRepeat) {
        /* Trick to reset/clear native browser form validation state */
        this.show = false
        this.$nextTick(() => { this.show = true })
        /* Fetching the data */
        storeAdminPassword(password)
          .then(() => {
            this.$emit('set-admin-password', true)
          })
          .catch(err => {
            this.error = err.message
            this.dismissCountDown = 6
          })
      } else {
        this.error = 'Passwords dont match!'
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
      this.form.adminPasswordRepeat = ''
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
