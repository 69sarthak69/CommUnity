
import { Loader } from '@googlemaps/js-api-loader'

const loader = new Loader({
  apiKey: 'AIzaSyAS7aBWvCP0nj1SlYs-H-grA1Zs35TE4QE',
  version: 'weekly',
  libraries: ['marker'],
  id: '__googleMapsScriptId', 
})

export default loader
