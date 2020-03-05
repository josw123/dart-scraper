import axios from 'axios'

const request_get = async (base, path) => {
  const url = `${base}${path}`
  const response = await axios.get(url)
  return response
}

const request_post = async (base, path, data) => {
  const url = `${base}${path}`
  if (data == null) {
    data = JSON.stringify({})
  }
  const response = await axios.post(url, data)
  return response
}

const request = {
  get: request_get,
  post: request_post,
}

export { request }