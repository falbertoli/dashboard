<template>
  <div>
    <table>
      <caption>{{ caption }}</caption>
      <thead>
        <tr>
          <th>Regulation Name</th>
          <th>Details</th>
          <th v-if="hasColumn('storage_gal_min')">Minimum Storage (Gal)</th>
          <th v-if="hasColumn('storage_gal_max')">Maximum Storage (Gal)</th>
          <th v-if="hasColumn('safety_distance_ft')">Safety Distance (ft)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in items" :key="item.regulation_name">
          <td>{{ item.regulation_name }}</td>
          <td>{{ item.regulation_info }}</td>
          <td v-if="hasColumn('storage_gal_min')">{{ item.storage_gal_min }}</td>
          <td v-if="hasColumn('storage_gal_max')">{{ item.storage_gal_max }}</td>
          <td v-if="hasColumn('safety_distance_ft')">{{ item.safety_distance_ft }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "RegulationsTable",
  props: {
    items: {
      type: Array,
      required: true,
    },
    caption: {
      type: String,
      required: true,
    },
  },
  methods: {
    hasColumn(column) {
      return this.items.some(item => column in item);
    },
  },
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

caption {
  font-weight: bold;
  margin-bottom: 10px;
  text-align: left;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}
</style>
