<template>
  <div>
    <table class="data-table">
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
          <td v-if="hasColumn('storage_gal_min')">{{ $formatNumber(item.storage_gal_min) }}</td>
          <td v-if="hasColumn('storage_gal_max')">{{ $formatNumber(item.storage_gal_max) }}</td>
          <td v-if="hasColumn('safety_distance_ft')">{{ $formatNumber(item.safety_distance_ft) }}</td>
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
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
  color: #e0e0e0;
}

.data-table th,
.data-table td {
  border: 1px solid #444;
  padding: 0.5rem;
  text-align: left;
}

.data-table th {
  background-color: rgba(255, 255, 255, 0.05);
  font-weight: bold;
  color: #64ffda;
}

.data-table tr:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.03);
}

.data-table tr:hover {
  background-color: #444;
}

caption {
  font-weight: bold;
  margin-bottom: 10px;
  text-align: left;
  color: #64ffda;
}
</style>
