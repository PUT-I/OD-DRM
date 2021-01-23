<template>
  <div>
    <b-form class="shadow-sm text-left text-bold p-2"><b>Users</b></b-form>

    <b-modal id="user-modal"
             ok-title="Save"
             size="xl"
             title="Add user"
             @ok="addUser">

      <b-form-group
          label="Username:"
          label-for="code-input">

        <b-form-input
            id="code-input"
            v-model="username"
            placeholder="Enter username"
            required/>
      </b-form-group>

      <b-form-group
          label="Password:"
          label-for="name-input">

        <b-form-input
            id="name-input"
            v-model="password"
            placeholder="Enter password"
            required/>
      </b-form-group>

      <b-form-checkbox
          id="authorized-checkbox"
          v-model="authorized">Authorized
      </b-form-checkbox>
    </b-modal>

    <div id="table-container" class="p-3" style="opacity: 0">
      <b-form class="shadow rounded bg-white p-3">
        <b-pagination
            v-model="currentPage"
            :per-page="perPage"
            :total-rows="users.length"
            aria-controls="detections-table"/>

        <b-table
            id="detections-table"
            :current-page="currentPage"
            :fields="user_fields"
            :items="users"
            :per-page="perPage"
            bordered
            class="shadow-sm"
            striped>

          <template #cell(action)="data">
            <b-button class="btn btn-danger shadow-sm"
                      style="width: 100px;"
                      type="button"
                      @click="deleteUser(data.item.userId, $event)">Delete
            </b-button>
          </template>

        </b-table>

        <b-button v-b-modal.user-modal
                  class="btn-success shadow">Add/Update user
        </b-button>
      </b-form>
    </div>
  </div>
</template>

<script>
import $ from 'jquery';
import UserService from "@/js/services/UserService";

export default {
  name: 'HelloWorld',
  data() {
    return {
      currentPage: 1,
      perPage: 10,
      users: [],
      username: "",
      password: "",
      authorized: true,
      user_fields: [
        {key: "userId", label: "Id", sortable: true},
        {key: "username", label: "Username", sortable: true},
        {key: "authorized", label: "Authorized", sortable: true},
        {key: "action", label: "Action", sortable: false}
      ]
    };
  },
  async mounted() {
    let data = (await UserService.getAllUsers()).data;

    console.log(JSON.stringify(data));

    this.users = data;
    console.log(this.users);

    $("#table-container").animate({"duration": 400, "opacity": "100%"});
  },
  methods: {
    async addUser() {
      const user = {
        username: this.username,
        password: this.password,
        authorized: this.authorized
      };

      let newUser = null;

      const filteredUser = this.users.filter((item) => item.username === user.username);
      if (filteredUser.length > 0) {
        newUser = (await UserService.updateUser(user)).data;
        this.users = this.users.filter((item) => item.username !== user.username);
      } else {
        newUser = (await UserService.addUser(user)).data;
      }
      this.users.push(newUser);

      this.username = "";
      this.password = "";
      this.authorized = true;
    },
    async deleteUser(id, event) {
      await UserService.deleteUser(id);

      $(event.target)
          .parent()
          .parent()
          .children('td')
          .animate({padding: 0})
          .wrapInner('<div />')
          .children()
          .slideUp(() => {
            $(this).closest('tr').remove();
          });
    }
  }
}
;
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
