const APIs = {
  path: "/api/v1/path",
  node: "/api/v1/node",
}

const GetActionPath = () => {
  return axios.get(APIs.path)
}

const SaveActionPath = (payload) => {
  return axios.post(APIs.path, payload)
}

const SaveNode = (payload) => {
  return axios.post(APIs.node, payload)
}


ELEMENT.locale(ELEMENT.lang.en)

new Vue({
  el: '#app',
  data: () => {
    return {
      activeTab: 0,
      currentNode: null,
      nodes: null,
      manualDescription: '',
      dialogFormVisible: false,
    }
  },
  created: function() {
    this.GetActionPath()
    this.currentNode = this.nodes[0]
  },
  methods: {
    GetActionPath() {
      const self = this
      GetActionPath().then((response) => {
        if (response.status === 200) {
          self.nodes = response.data.nodes
          if (self.nodes) {
            self.currentNode = self.nodes[self.activeTab]
          }
          return Promise.resolve(response.data.nodes)
        }
        self.$message.error("Get Action Path failed, please try again")
        return Promise.reject(response.status)
      })
    },
    saveActionPath() {
      const self = this

      if (self.manualDescription.length < 20) {
        self.$message.error("Your description is too short, please describe more :(")
        return
      }

      urls = []
      for (i = 0; i < self.nodes.length; i++) {
        urls.push(self.nodes[i].url)
      }
      SaveActionPath({
        path: urls,
        manual_desc: self.manualDescription
      }).then((response) => {
        console.log(response)
        self.$message.success(response.data.message + " Your task has been updated.")
        self.GetActionPath()
        self.manualDescription = ''
      })
    },
    changeActionPath() {
      const self = this
      self.$message.success("Your task has been updated.")
      self.GetActionPath()
      self.manualDescription = ''
    },
    editCurrentNode() {
      this.dialogFormVisible = true
    },
    saveCurrentNode() {
      const self = this

      if (self.currentNode.meta.length < 5) {
        self.$message.error("Your metadata is too short, please describe more :(")
      }
      self.currentNode.meta = [self.currentNode.meta]
      if (self.currentNode.keywords.length < 5) {
        self.$message.error("Your keywords are too less, please describe more :(")
      }
      self.currentNode.keywords = [self.currentNode.keywords]
      if (self.currentNode.manual_desc.length < 5) {
        self.$message.error("Your description is too short, please describe more :(")
      }

      SaveNode(self.currentNode).then((response) => {
        console.log(response)
        self.$message.success(response.message)
        self.dialogFormVisible = false
      }).catch((error) => {
        self.$message.error(error.response.message)
      })
    },
    tabName(index) {
      return `${index}`
    },
    tabIndex(index) {
      if (index === 0) {
        return 'Starting'
      }
      return 'Step ' + index
    },
    filterSourceCode(source) {
      return source
      // .replace(/(\/\*[\w\'\s\r\n\*]*\*\/)|(\/\/[\w\s\']*)|(\<![\-\-\s\w\>\/]*\>)/g, '')
      // .replace(/\/\*[\s\S]*?\*\//g, '')
      .replace(/\/\*[\s\S]*?\*\/|([^\\:]|^)\/\/.*$/gm, '$1')
      .replace(/(^[ \t]*\n)/gm, '')
      .replace(/<!--[\s\S]*?-->/g, '')
    },
    tabClickHandler(tab) {
      this.activeTab = tab.index
      this.currentNode = this.nodes[parseInt(tab.index, 10)]
    },
  }
})