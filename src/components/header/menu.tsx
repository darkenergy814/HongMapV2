import React from "react";
import styled from "styled-components";

function SearchingMenu() {
    return(
        <MenuArea>
            <StartingPointBox type="text" placeholder={"출발지를 입력하세요"}></StartingPointBox>
            <EndPointBox type="text" placeholder={"도착지를 입력하세요"}></EndPointBox>
            <FindingWayBox>길찾기</FindingWayBox>
        </MenuArea>
    )
}

function ClubMenu(){
    return(
        <MenuArea></MenuArea>
    )
}

export {SearchingMenu, ClubMenu};

const MenuArea = styled.div`
  width: 366px;
  height: 260px;
`

const StartingPointBox = styled.input`
  position: absolute;
  left: 35px;
  Top: 18px;
  width: 297px;
  height: 55px;
  border: none;
  border-radius: 16px;
  color: #BCBCBC;
  &::placeholder {
    color: #BCBCBC;
  }
  font-size: medium;
  background-color: #F3F4FF;
  text-align: center;
`

const EndPointBox = styled.input`
  position: absolute;
  left: 35px;
  Top: 83px;
  width: 297px;
  height: 55px;
  border: none;
  border-radius: 16px;
  color: #BCBCBC;
  &::placeholder {
    color: #BCBCBC;
  }
  font-size: medium;
  background-color: #F3F4FF;
  text-align: center;
`

const FindingWayBox = styled.div`
  position: absolute;
  left: 35px;
  Top: 151px;
  width: 297px;
  height: 40px;
  border: none;
  border-radius: 10px;
  background-color: #9CA6FF;
  color: #FFFFFF;
  cursor: pointer;
  font-size: medium;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
`
