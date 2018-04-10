<template>
  <v-content style="height: 90vh">
    <v-container fluid style="height: 90vh">
      <v-form v-model="valid">
        <v-text-field
          label="Amazon URL"
          v-model="url"
          :rules="urlRules"
          required
        ></v-text-field>

      </v-form>
      <v-flex fluid><p style="color: red">{{ error }}</p></v-flex>


      <v-flex fluid>
        <v-card style="height: 80vh">
          <v-layout column style="height: 70vh">
            <v-toolbar color="white" dark>
              <v-toolbar-title>App Info</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-list>
              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Name: {{app.name}}</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Version: {{app.version}}</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>

              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Original Release Date: {{app.original_release_date | formatDate}}</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>
              <v-list-tile>
                <v-list-tile-content>
                  <v-list-tile-title>Latest Release Date: {{app.latest_release_date | formatDate}}</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
            <v-toolbar color="white" dark>
              <v-toolbar-title>Changelog</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-list>
              <v-list-tile v-for="item in app.change_log">

                <v-list-tile-content>
                  <v-list-tile-title>{{item}}</v-list-tile-title>
                </v-list-tile-content>
              </v-list-tile>
            </v-list>
          </v-layout>
        </v-card>
      </v-flex>

    </v-container>
  </v-content>
</template>

<script type="text/babel">
  import axios from 'axios'

  axios.defaults.baseURL = document.referrer + 'api/';

  export default {
    name: 'HelloWorld',
    data: () => ({
      error: "",
      valid: false,
      url: '',
      urlRules: [
        v => !!v || 'Amazon URL is required'
      ],
      app: {
        name: "",
        version: "",
        change_log: "",
        original_release_date: "",
        latest_release_date: "",
      }
    }),
    watch: {
      'url'(query, from) {
        clearTimeout(this.timeOut);
        this.timeOut = setTimeout(() => {
          this.postQuery()
        }, 250);

      }
    },
    methods: {
      postQuery() {
        return axios.post("query/", {
          query_string: this.url
        }).then(response => {
          console.log(response)
          this.error = ""
          this.app.name = response.data.app_name
          this.app.version = response.data.app_version
          this.app.change_log = response.data.change_log
          this.app.original_release_date = response.data.original_release_date
          this.app.latest_release_date = response.data.latest_release_date
        }).catch(response => {
          this.error = "You have entered an invalid Amazon App Store URL. Please try again and ensure to include https://."
          console.log(response.response)
        })
      },
      updateUI(query) {
        this.getResources('people', query).then(response => {
          this.data.people = response.data
        }).catch(function (e) {
          alert(e)
        })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
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
</style>
