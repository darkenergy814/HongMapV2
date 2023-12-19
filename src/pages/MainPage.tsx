import React from "react";
import styled from "styled-components";
import Header from "../components/header/header";
import Map from "../components/body/body"

function MainPage(){
    return(
        <MainPageContainer>
            <Header />
            <Map />
        </MainPageContainer>
    )
}

export default MainPage;

const MainPageContainer = styled.div`
  width: 100%;
  height: 100%;
`
