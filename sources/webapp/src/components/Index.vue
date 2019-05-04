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
                <b-col sm="10">
                    <div>
                        <b-form-file multiple v-model="file" v-bind:state="Boolean(file)" accept="image/*" placeholder="Choose a file..." drop-placeholder="Drop file here...">
                           <template slot="file-name" slot-scope="{ names }">
                             <b-badge variant="dark">{{ names[0] }}</b-badge>
                             <b-badge v-if="names.length > 1" variant="dark" class="ml-1"> + {{ names.length - 1 }} More files</b-badge>
                           </template>
                        </b-form-file>
                    </div>
                </b-col>
            </b-row>
            <b-row align-v="start" align-h="around">
                <b-col sm="12">
                    <br />
                </b-col>
            </b-row>
        </div>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'Info',
  props: ['loading', 'data', 'labels'],
  data() {
    return {
      file: null
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
a {
  color: #42b983;
}
.processesTable{
  font-size: 14px;
}
.container {
  max-width: 800px;
  margin:  0 auto;
}
.Chart {
  background: #FFFFFF;
}
.Chart h2 {
  margin-top: 0;
  padding: 15px 0;
  border-bottom: 1px solid #323d54;
}
</style>
