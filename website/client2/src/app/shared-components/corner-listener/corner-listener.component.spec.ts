import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CornerListenerComponent } from './corner-listener.component';

describe('CornerListenerComponent', () => {
  let component: CornerListenerComponent;
  let fixture: ComponentFixture<CornerListenerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CornerListenerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CornerListenerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
