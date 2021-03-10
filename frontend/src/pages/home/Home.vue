<template>
  <div class="container">
    <div class="row justify-content-center mt-4">
      <div class="col-6">
        <div class="form-group">
          <div class="input-group">
            <input
              type="input"
              class="form-control m-1"
              placeholder="Назавание новой комнаты"
              v-model="roomCreateName"
            />
            <button
              class="btn btn-success m-1"
              v-on:click="backendRoomCreate()"
            >
              Создать
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="row mt-4">
      <div v-for="room in rooms" :key="room.id" class="col-4">
        <div class="card">
          <h4 class="card-header">{{ room.name }}</h4>
          <button
            class="btn btn-danger"
            v-on:click="backendRoomRemove(room.id)"
          >
            Удалить комнату
          </button>
          <div class="card-body">
            <h5 class="card-title">Пользователи в комнате:</h5>
            <p
              class="card-text"
              v-for="user in room.room_permission"
              :key="user.id"
            >
              - {{ user.user.email }}
            </p>
            <button class="btn btn-primary" v-on:click="enterRoom(room.id)">
              Зайти
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: "Home",
  components: {},
  data: () => ({
    rooms: Object,
    roomCreateName: "",
  }),
  async mounted() {
    this.reload();
  },
  methods: {
    async reload() {
      const response = await fetch("/task/room/list/");
      if (response.ok) {
        this.rooms = await response.json();
      } else {
        console.log("errors!");
      }
    },
    enterRoom(id) {
      localStorage.setItem("room", id);
      this.$router.push({ name: "room" });
    },
    async backendRoomCreate() {
      const response = await fetch(`/task/room/form/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: this.roomCreateName,
        }),
      });
      if (response.ok) {
        this.columnCreateName = "";
        this.reload();
      }
    },
    async backendRoomRemove(target) {
      const response = await fetch(`/task/room/edit/${target}/`, {
        method: "DELETE",
      });
      if (response.ok) {
        this.reload();
      }
    },
  },
};
</script>

<style>
</style>