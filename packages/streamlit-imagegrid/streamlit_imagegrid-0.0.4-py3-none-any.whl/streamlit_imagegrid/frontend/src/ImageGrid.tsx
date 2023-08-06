import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection
} from "streamlit-component-lib";
import Gallery from "react-grid-gallery";
import React, { ReactNode } from "react"
class ImageGrid extends StreamlitComponentBase{

    IsValidJSONString(str:any):boolean {
    if (str.hasOwnProperty('src')) {
        return true;
      }
    return false;
  }


    public render = (): ReactNode => {
    const imageClick = (e: any) => {
          Streamlit.setComponentValue(urls[e])
        }
    const urls = this.props.args["urls"];
    const zoom = this.props.args["zoom"];
    const height = this.props.args["height"]

    var output_urls = []

    if (urls.length >0 )
    {
    if (this.IsValidJSONString(urls[0])){
      output_urls= urls.map(x => { return ({"caption":"Yeah","src":x['src'],"thumbnail":x['src'],"thumbnailWidth":x['width'],"thumbnailHeight":x['height']})})
    }else{
      output_urls = urls.map(x => {return({"src": x,"thumbnail":x});});
    }

    }
    else{
      return "None"
    }
    return (<div style={{height: height, overflowY:"auto"}}>

      <Gallery style={{width:"auto"}} maxRows={100} enableImageSelection={true} onClickThumbnail={imageClick} rowHeight={zoom} images={output_urls}/>

      </div>)

    }
}

export default withStreamlitConnection(ImageGrid)
