import React from "react";
import styled from "styled-components";
import hongMap from "../../static/logo/hongikMapv2.jpg";

function Body() {
    return(
        <BodyContainer>
            <MapArea src={hongMap}/>
        </BodyContainer>
    )
}

export default Body;

const BodyContainer = styled.div`
  display: flex;
  width: 100%;
  justify-content: center;
`

const MapArea = styled.img`
  position: absolute;
  margin: auto;
  width: 80%;
  z-index: -2;
`
